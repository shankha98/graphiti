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

from typing import Any, Protocol, TypedDict

from .models import Message, PromptFunction, PromptVersion


class Prompt(Protocol):
    system_instruction: PromptVersion
    episode_content: PromptVersion


class Versions(TypedDict):
    system_instruction: PromptFunction
    episode_content: PromptFunction


def system_instruction(context: dict[str, Any]) -> list[Message]:
    """Generate the system instruction for the graph agent."""
    return [
        Message(
            role="system",
            content="""You are an expert Knowledge Graph engineer specialized in extracting structured information from text.

**Your Role:**
- Extract entities (people, places, concepts) and relationships between them
- Build an accurate, temporally-aware knowledge graph
- Handle ambiguity through search and verification

**Your Capabilities:**
1. **Search Tool**: Query existing nodes and edges to avoid duplicates and gather context
2. **Planning**: Decide when you need more information before extraction
3. **Extraction**: Generate structured GraphUpdate with nodes and edges

**Process:**
1. Analyze the episode content
2. If entities might already exist OR context is unclear:
   - Set `needs_more_info=True`
   - Provide specific `search_queries` to find relevant entities
3. After gathering context (or if no search needed):
   - Set `is_final=True`
   - Provide complete `GraphUpdate` with all nodes and edges

**Critical Rules:**
- **Deduplication**: If search results match an entity you're extracting, use its `uuid` in ExtractedNode
- **Consistency**: Ensure edge `source` and `target` match node `name` values exactly
- **Completeness**: Include ALL relevant entities and relationships from the current content
- **Temporal Awareness**: Extract time information when present (valid_at, invalid_at for edges)
- **No Hallucination**: Only extract information explicitly or implicitly stated in the content

**Entity Extraction:**
- Extract significant entities mentioned explicitly or implicitly
- Resolve pronouns to actual names using context
- Use full names when available, avoid abbreviations
- DO NOT extract dates, times, or temporal information as entities
- DO extract: people, organizations, locations, concepts, projects, products

**Relationship Extraction:**
- Extract factual relationships between distinct entities
- Use SCREAMING_SNAKE_CASE for relation types (e.g., FOUNDED, WORKS_AT, MET)
- Paraphrase facts naturally in the fact field, don't quote verbatim
- Include temporal information for edges when available
- Don't create duplicate or redundant relationships

**Temporal Information:**
- Use ISO 8601 format with UTC (e.g., 2025-04-30T14:30:00Z)
- Set `valid_at` when a relationship starts or is ongoing
- Set `invalid_at` when a relationship ends
- Leave both null if no temporal information is stated
- Resolve relative time references using the reference time provided

**Language**: Return extracted information in the same language as the source content.
""",
        )
    ]


def episode_content(context: dict[str, Any]) -> list[Message]:
    """Format episode content for the agent."""
    sections = []

    # Entity types
    if context.get("entity_types"):
        sections.append(f"<ENTITY_TYPES>\n{context['entity_types']}\n</ENTITY_TYPES>")

    # Edge types
    if context.get("edge_types"):
        sections.append(f"<EDGE_TYPES>\n{context['edge_types']}\n</EDGE_TYPES>")

    # Previous episodes for context
    if context.get("previous_episodes"):
        sections.append(
            f"<PREVIOUS_EPISODES>\nThe following episodes provide context. "
            f"Use them to disambiguate references but only extract entities and relationships from the CURRENT episode.\n"
            f"{context['previous_episodes']}\n</PREVIOUS_EPISODES>"
        )

    # Current episode content
    sections.append(
        f"<EPISODE_CONTENT>\n{context['episode_content']}\n</EPISODE_CONTENT>"
    )

    # Source description
    sections.append(
        f"<SOURCE>\n{context.get('source_description', 'Unknown')}\n</SOURCE>"
    )

    # Reference timestamp
    sections.append(
        f"<REFERENCE_TIME>\n{context.get('reference_time', 'Unknown')} (ISO 8601 UTC)\n</REFERENCE_TIME>"
    )

    # Instructions
    sections.append(
        "\nAnalyze this content and determine if you need to search for context, "
        "or if you can directly extract entities and relationships.\n"
        "\nAny extracted information should be returned in the same language as it was written in."
    )

    return [Message(role="user", content="\n\n".join(sections))]


versions: Versions = {
    "system_instruction": system_instruction,
    "episode_content": episode_content,
}
