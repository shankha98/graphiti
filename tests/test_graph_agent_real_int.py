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
import pytest
from datetime import datetime, timezone

from graphiti_core.graphiti import Graphiti
from graphiti_core.nodes import EpisodeType
from tests.helpers_test import GraphProvider

pytestmark = pytest.mark.integration
pytest_plugins = ("pytest_asyncio",)

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_add_episode_with_real_agent(graph_driver):
    """Integration test for add_episode using real Gemini agent."""
    if graph_driver.provider == GraphProvider.FALKORDB:
        pytest.skip("Skipping as tests fail on Falkordb")

    graphiti = Graphiti(graph_driver=graph_driver)
    await graphiti.build_indices_and_constraints()

    episode_body = "Alice met Bob at the park. They discussed the new project."
    reference_time = datetime.now(timezone.utc)

    # Add episode using the real GraphAgent with Gemini
    result = await graphiti.add_episode(
        name="Meeting in the park",
        episode_body=episode_body,
        source_description="A conversation log",
        reference_time=reference_time,
        source=EpisodeType.message,
    )

    # Verify results
    assert result is not None
    assert len(result.nodes) > 0, "Should have extracted at least one node"

    # Log extracted entities for debugging
    logger.info(f"Extracted {len(result.nodes)} nodes:")
    for node in result.nodes:
        logger.info(f"  - {node.name} ({node.labels})")

    logger.info(f"Extracted {len(result.edges)} edges:")
    for edge in result.edges:
        logger.info(f"  - {edge.name}: {edge.fact}")

    # At minimum we should have some entities extracted
    assert len(result.nodes) >= 1, "Expected at least 1 entity node"

    await graphiti.close()
