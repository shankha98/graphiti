"""
Copyright 2024, Zep Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
import typing
from datetime import datetime

from pydantic import BaseModel, Field

from graphiti_core.edges import EntityEdge
from graphiti_core.graphiti_types import GraphitiClients
from graphiti_core.llm_client.config import ModelSize
from graphiti_core.nodes import EntityNode, EpisodicNode
from graphiti_core.prompts.models import Message
from graphiti_core.search.search import search
from graphiti_core.search.search_config_recipes import (
    EDGE_HYBRID_SEARCH_RRF,
    NODE_HYBRID_SEARCH_RRF,
)
from graphiti_core.search.search_filters import SearchFilters
from graphiti_core.utils.datetime_utils import utc_now

logger = logging.getLogger(__name__)


class SearchQuery(BaseModel):
    """A search query to find relevant nodes and edges in the graph."""

    query: str = Field(..., description="The search query string.")
    search_type: typing.Literal["node", "edge"] = Field(
        ..., description="Whether to search for nodes or edges."
    )


class AgentPlan(BaseModel):
    """The agent's plan for processing the episode."""

    thoughts: str = Field(
        ...,
        description="The agent's reasoning about the episode and what needs to be done.",
    )
    search_queries: list[SearchQuery] = Field(
        default_factory=list,
        description="List of search queries to execute to gather context.",
    )
    needs_more_info: bool = Field(
        ...,
        description="True if the agent needs to search for more information before updating the graph.",
    )


class ExtractedNode(BaseModel):
    name: str
    labels: list[str]
    summary: str | None = None
    uuid: str | None = Field(
        None, description="The UUID of the existing node, if found."
    )


class ExtractedEdge(BaseModel):
    source: str
    target: str
    relation: str
    fact: str
    valid_at: datetime | None = None
    invalid_at: datetime | None = None


class GraphUpdate(BaseModel):
    """The final update to the graph."""

    thoughts: str = Field(..., description="Reasoning for the graph updates.")
    nodes: list[ExtractedNode] = Field(
        default_factory=list, description="List of nodes to add or update."
    )
    edges: list[ExtractedEdge] = Field(
        default_factory=list, description="List of edges to add or update."
    )
    is_final: bool = Field(
        ...,
        description="True if this is the final update and no more steps are needed.",
    )


class GraphAgent:
    """
    A Gemini-powered agent that processes episodes and updates the graph.
    It uses a loop to analyze content, search for context, and then generate updates.
    """

    def __init__(self, clients: GraphitiClients):
        self.clients = clients
        self.llm_client = clients.llm_client

    async def process_episode(
        self,
        episode: EpisodicNode,
        previous_episodes: list[EpisodicNode],
        entity_types: dict[str, type[BaseModel]] | None = None,
        edge_types: dict[str, type[BaseModel]] | None = None,
    ) -> tuple[list[EntityNode], list[EntityEdge]]:
        """
        Process an episode using the agent loop.
        """

        # Initial context
        context_messages = [
            Message(
                role="system",
                content=(
                    "You are an expert Knowledge Graph engineer. Your goal is to extract entities and relationships "
                    "from the given episode content and update the graph.\n"
                    "You have access to a search tool to find existing nodes and edges.\n"
                    "First, analyze the content and decide if you need to search for existing entities to avoid duplicates "
                    "or to understand the context better.\n"
                    "If you need more info, output a plan with `needs_more_info=True` and provide `search_queries`.\n"
                    "If you have enough info, output a `GraphUpdate` with `is_final=True` containing the nodes and edges.\n"
                    "IMPORTANT: If you find an existing node in the search results that matches an entity you are extracting, "
                    "you MUST include its `uuid` in the `ExtractedNode` object. This is critical for deduplication.\n"
                    "For edges, ensure the `source` and `target` names match the `name` of the nodes in your `nodes` list."
                ),
            ),
            Message(
                role="user",
                content=self._build_initial_prompt(
                    episode, previous_episodes, entity_types, edge_types
                ),
            ),
        ]

        max_steps = 5
        current_step = 0

        extracted_nodes: list[EntityNode] = []
        extracted_edges: list[EntityEdge] = []

        while current_step < max_steps:
            logger.info(f"Agent step {current_step + 1}/{max_steps}")

            # Let's use the `AgentPlan` for the first step.
            if current_step == 0:
                response = await self.llm_client.generate_response(
                    context_messages,
                    response_model=AgentPlan,
                    model_size=ModelSize.medium,  # Use a capable model
                    group_id=episode.group_id,
                    prompt_name="agent.plan",
                )
                plan = AgentPlan(**response)
                logger.info(f"Agent Plan: {plan.thoughts}")

                context_messages.append(Message(role="model", content=str(response)))

                if not plan.needs_more_info:
                    # Jump to final update generation
                    break

                # Execute search
                search_results = await self._execute_searches(
                    plan.search_queries, episode.group_id
                )
                context_messages.append(
                    Message(
                        role="user",
                        content=f"Search Results:\n{search_results}\n\nNow provide the final GraphUpdate.",
                    )
                )
            else:
                # Subsequent steps (should be final update)
                break

            current_step += 1

        # Final Step: Generate GraphUpdate
        response = await self.llm_client.generate_response(
            context_messages,
            response_model=GraphUpdate,
            model_size=ModelSize.medium,
            group_id=episode.group_id,
            prompt_name="agent.update",
        )
        update = GraphUpdate(**response)
        logger.info(f"Agent Update: {update.thoughts}")

        # Convert to internal types
        extracted_nodes = []
        name_to_node_map: dict[str, EntityNode] = {}

        for n in update.nodes:
            # If uuid is provided, we assume it's an existing node.
            # However, we still create an EntityNode object for it, but we need to handle it carefully.
            # If it's an existing node, we might be updating it.
            # If uuid is NOT provided, it's a new node.

            # Note: In the current Graphiti architecture, we usually return a list of nodes to be upserted.
            # If we provide a UUID, the driver should handle the upsert/merge.

            # Create EntityNode - if UUID is provided, pass it; otherwise let EntityNode generate new one
            node_params = {
                "name": n.name,
                "labels": n.labels,
                "summary": n.summary or "",
                "group_id": episode.group_id,
                "created_at": utc_now(),
            }
            if n.uuid:
                node_params["uuid"] = n.uuid

            node = EntityNode(**node_params)
            extracted_nodes.append(node)
            name_to_node_map[n.name] = node

        extracted_edges = []
        for e in update.edges:
            source = name_to_node_map.get(e.source)
            target = name_to_node_map.get(e.target)

            # If source or target are missing from the extracted nodes, it might be because
            # the agent didn't include them in the `nodes` list but they exist in the graph.
            # Ideally, the agent should include ALL referenced nodes in the `nodes` list,
            # even if they are just being referenced (with their UUIDs).
            # If they are missing, we can't easily resolve them without another search or assumption.
            # For now, we'll log a warning and skip.

            if source and target:
                extracted_edges.append(
                    EntityEdge(
                        source_node_uuid=source.uuid,  # type: ignore
                        target_node_uuid=target.uuid,  # type: ignore
                        name=e.relation,
                        fact=e.fact,
                        group_id=episode.group_id,
                        created_at=utc_now(),
                        valid_at=e.valid_at,
                        invalid_at=e.invalid_at,
                        episodes=[episode.uuid],
                    )
                )
            else:
                logger.warning(
                    f"Skipping edge {e.source} -> {e.target}: Nodes not found in extracted set. "
                    f"Source found: {source is not None}, Target found: {target is not None}"
                )

        return extracted_nodes, extracted_edges

    def _build_initial_prompt(
        self,
        episode: EpisodicNode,
        previous_episodes: list[EpisodicNode],
        entity_types: dict[str, type[BaseModel]] | None,
        edge_types: dict[str, type[BaseModel]] | None,
    ) -> str:
        prompt = f"Episode Content:\n{episode.content}\n\n"
        prompt += f"Source: {episode.source_description}\n"
        prompt += f"Timestamp: {episode.valid_at}\n\n"

        if previous_episodes:
            prompt += "Previous Context:\n"
            for prev in previous_episodes[-3:]:  # Last 3 for brevity
                prompt += f"- {prev.content}\n"
            prompt += "\n"

        if entity_types:
            prompt += "Allowed Entity Types:\n"
            for name, model in entity_types.items():
                prompt += f"- {name}: {model.__doc__}\n"
            prompt += "\n"

        if edge_types:
            prompt += "Allowed Edge Types:\n"
            for name, model in edge_types.items():
                prompt += f"- {name}: {model.__doc__}\n"
            prompt += "\n"

        return prompt

    async def _execute_searches(self, queries: list[SearchQuery], group_id: str) -> str:
        results_text = ""
        for q in queries:
            if q.search_type == "node":
                results = await search(
                    self.clients,
                    q.query,
                    group_ids=[group_id],
                    config=NODE_HYBRID_SEARCH_RRF,
                    search_filter=SearchFilters(),
                )
                results_text += f"Query '{q.query}' (Nodes):\n"
                for node in results.nodes[:5]:
                    results_text += f"- Name: {node.name}, UUID: {node.uuid}, Labels: {', '.join(node.labels)}, Summary: {node.summary}\n"
            else:
                results = await search(
                    self.clients,
                    q.query,
                    group_ids=[group_id],
                    config=EDGE_HYBRID_SEARCH_RRF,
                    search_filter=SearchFilters(),
                )
                results_text += f"Query '{q.query}' (Edges):\n"
                for edge in results.edges[:5]:
                    results_text += f"- {edge.source_node_uuid} -> {edge.target_node_uuid}: {edge.fact}\n"
            results_text += "\n"
        return results_text
