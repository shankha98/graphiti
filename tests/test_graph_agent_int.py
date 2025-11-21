"""
Copyright 2024, Zep Software, Inc.

Licensed under the Apache License, Version 20 (the "License");
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
import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

from graphiti_core.graphiti import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.llm_client import LLMClient
from graphiti_core.utils.maintenance.graph_agent import (
    AgentPlan,
    GraphUpdate,
    ExtractedNode,
    ExtractedEdge,
)
from tests.helpers_test import GraphProvider

pytestmark = pytest.mark.integration
pytest_plugins = ("pytest_asyncio",)

logger = logging.getLogger(__name__)


class MockLLMClient(LLMClient):
    def __init__(self):
        self.generate_response = AsyncMock()
        self.set_tracer = MagicMock()
        super().__init__(config=None)

    async def _generate_response(
        self, messages, response_model=None, max_tokens=None, model_size=None
    ):
        return {}


@pytest.mark.asyncio
async def test_add_episode_with_agent(graph_driver, mock_embedder):
    if graph_driver.provider == GraphProvider.FALKORDB:
        pytest.skip("Skipping as tests fail on Falkordb")

    # Setup Mock LLM
    mock_llm = MockLLMClient()

    # Mock responses
    # 1. AgentPlan: No more info needed
    plan_response = AgentPlan(
        thoughts="I have enough information.",
        plan="Extracting nodes and edges directly.",
        search_queries=[],
        needs_more_info=False,
    )

    # 2. GraphUpdate: Return extracted data
    update_response = GraphUpdate(
        thoughts="I have extracted all necessary information.",
        nodes=[
            ExtractedNode(
                name="Alice", labels=["Person"], summary="A person", uuid="uuid-alice"
            ),
            ExtractedNode(
                name="Bob", labels=["Person"], summary="A person", uuid="uuid-bob"
            ),
        ],
        edges=[
            ExtractedEdge(
                source="Alice",
                target="Bob",
                relation="MET",
                fact="Alice met Bob at the park",
            )
        ],
        is_final=True,
    )

    # Mock returns dicts, not Pydantic instances
    mock_llm.generate_response.side_effect = [
        plan_response.model_dump(),
        update_response.model_dump(),
    ]

    graphiti = Graphiti(
        graph_driver=graph_driver, llm_client=mock_llm, embedder=mock_embedder
    )
    await graphiti.build_indices_and_constraints()

    episode_body = "Alice met Bob at the park. They discussed the new project."
    reference_time = datetime.now(timezone.utc)

    # Add episode
    result = await graphiti.add_episode(
        name="Meeting in the park",
        episode_body=episode_body,
        source_description="A conversation log",
        reference_time=reference_time,
        source=EpisodeType.message,
    )

    # Verify results
    assert result is not None
    assert len(result.nodes) == 2
    assert len(result.edges) == 1

    alice_node = next((n for n in result.nodes if "Alice" in n.name), None)
    bob_node = next((n for n in result.nodes if "Bob" in n.name), None)

    assert alice_node is not None
    assert bob_node is not None

    # Check for edge between Alice and Bob
    edge = result.edges[0]
    assert edge.source_node_uuid == alice_node.uuid
    assert edge.target_node_uuid == bob_node.uuid
    assert edge.name == "MET"

    await graphiti.close()
