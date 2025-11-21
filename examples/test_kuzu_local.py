"""
Simple test script to initialize Graphiti with Kuzu and add an episode.
Run with: uv run python test_kuzu_local.py
"""

import json
import asyncio
import logging
from datetime import datetime, timezone


from graphiti_core import Graphiti
from graphiti_core.driver.kuzu_driver import KuzuDriver
from graphiti_core.nodes import EpisodeType

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Initialize Graphiti with Kuzu and add a test episode."""

    # Kuzu database path (local file, not directory)
    # Kuzu expects a file path or ":memory:" for in-memory database
    kuzu_db_path = "./kuzu_test.db"

    logger.info(f"Initializing Graphiti with Kuzu database at: {kuzu_db_path}")

    # Create Kuzu driver
    # Use the database file path
    # For in-memory database, use ":memory:" instead
    kuzu_driver = KuzuDriver(
        db=kuzu_db_path,
        max_concurrent_queries=1,
    )

    # Initialize Graphiti with Kuzu driver
    graphiti = Graphiti(
        graph_driver=kuzu_driver,
        # Optional: Specify LLM and embedder if you want to override defaults
        # llm_client=your_llm_client,
        # embedder=your_embedder,
    )

    try:
        # Build indices and constraints
        logger.info("Building indices and constraints...")
        await graphiti.build_indices_and_constraints()

        # Prepare test episode
        episode_body = {
            "_id": {"$oid": "6909f81d663f38c8bf0f8803"},
            "org_id": "98a167ba-210e-4c11-b46e-12212e1d0d89",
            "metadata": {
                "sync_time": "2025-11-05T08:30:59.650208+00:00",
                "sync_type": "incremental",
                "previous_sync_time": "2025-11-04T16:41:31.004032+00:00",
                "pages": {
                    "26a77667-4236-80f5-a57d-ec3f26294e75": {
                        "last_edited_time": "2025-11-04T16:19:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Fundraising - Emails",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "26277667-4236-8011-b106-d6b05be049dd": {
                        "last_edited_time": "2025-10-24T13:50:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Rice - Backed by Techstars (London 2024)",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "28f77667-4236-808f-bea7-d477a7532a23": {
                        "last_edited_time": "2025-10-21T08:40:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Rice - Backed by Techstars",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "28777667-4236-807f-a17f-d5dd3ea369e9": {
                        "last_edited_time": "2025-10-09T14:00:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Sales Memo",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "27f77667-4236-8037-a3c1-f40e62e68aa8": {
                        "last_edited_time": "2025-10-01T13:16:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Investor Updates",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "27f77667-4236-80aa-b982-f1a5b12cff9a": {
                        "last_edited_time": "2025-10-01T08:06:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Q3’2025 - Major Upsides",
                        "parent_type": "page_id",
                        "parent_id": "27f77667-4236-8037-a3c1-f40e62e68aa8",
                    },
                    "27b77667-4236-8009-8d6f-d077d410bb90": {
                        "last_edited_time": "2025-09-27T09:00:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Measurement and Optimisation - Advanced",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-803a-94fe-effab636eee3": {
                        "last_edited_time": "2025-09-27T09:00:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Scaling and Automation",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-8098-812c-da6479befd5d": {
                        "last_edited_time": "2025-09-27T08:59:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Relationship Nurturing Systems",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-80f0-89c2-ff60bba74ede": {
                        "last_edited_time": "2025-09-27T08:59:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Sales Intelligence and Research",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-80f0-b053-ee8e87848560": {
                        "last_edited_time": "2025-09-27T08:59:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Content Multiplication Strategies",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-80a8-8619-d19b122515d4": {
                        "last_edited_time": "2025-09-27T08:59:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Unconventional Channels",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-8096-9ccb-d883d9582c4b": {
                        "last_edited_time": "2025-09-27T08:58:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Industry Specific Channels",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-8075-902b-cd4f8547b3d6": {
                        "last_edited_time": "2025-09-27T08:58:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Advanced / Creative Channels",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-80f9-af38-de06feb56ccc": {
                        "last_edited_time": "2025-09-27T08:58:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Execution Timeline",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-80c9-982d-fa223722aef4": {
                        "last_edited_time": "2025-09-27T08:57:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Tools and Budget Breakdown",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-80a7-8911-e5af87206181": {
                        "last_edited_time": "2025-09-27T08:57:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Measurement and Optimisation",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-8086-96f6-e67df6194792": {
                        "last_edited_time": "2025-09-27T08:57:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Partnership Channels",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-80b3-9bd1-da30bd691212": {
                        "last_edited_time": "2025-09-27T08:57:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Digital Prospecting",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-80a7-80f8-e584319230b2": {
                        "last_edited_time": "2025-09-27T08:56:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Event and Conferences",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-80a4-8cda-c8a4b1225767": {
                        "last_edited_time": "2025-09-27T08:56:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Free / Low Cost Lead Gen",
                        "parent_type": "page_id",
                        "parent_id": "27b77667-4236-807d-84ca-e6c33d3e2058",
                    },
                    "27b77667-4236-807d-84ca-e6c33d3e2058": {
                        "last_edited_time": "2025-09-27T08:54:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Playbook - Rice",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "27a77667-4236-8038-84d4-d3835c91b710": {
                        "last_edited_time": "2025-09-26T10:02:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Prafull Sharma",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "26b77667-4236-807b-b0c5-fe514b187046": {
                        "last_edited_time": "2025-09-24T10:09:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Anirban Halder",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "27877667-4236-806a-897d-f1a1d5115d79": {
                        "last_edited_time": "2025-09-24T09:53:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Kim Nilsson",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "27877667-4236-8035-ac11-ea41eaddffa6": {
                        "last_edited_time": "2025-09-24T09:47:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Gustavo Imhof",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "27377667-4236-80db-8ad6-f87730cc4b1c": {
                        "last_edited_time": "2025-09-24T09:39:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Claudia Tersigni",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "27277667-4236-8019-86a2-c30f4434f73a": {
                        "last_edited_time": "2025-09-24T09:29:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Aroop Zutshi",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "26b77667-4236-80aa-b131-e6cb8dd45418": {
                        "last_edited_time": "2025-09-24T09:26:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Charlie Cannel",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "27377667-4236-80ee-8e16-f1c016214d7a": {
                        "last_edited_time": "2025-09-19T12:16:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Rice - Backed by Techstars (London 2024) - Pre",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "26b77667-4236-8016-a062-d7ab27ecc86e": {
                        "last_edited_time": "2025-09-19T11:32:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Nikhil Kartha",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "26b77667-4236-80b6-9967-d9d66e9b1646": {
                        "last_edited_time": "2025-09-19T11:12:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Mariana Simoes",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "26b77667-4236-804a-898f-dee5513345a8": {
                        "last_edited_time": "2025-09-19T11:10:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Simon Morley",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "27277667-4236-80b1-b469-f7b6a0cb85ba": {
                        "last_edited_time": "2025-09-18T09:52:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Rohit Garg",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "26b77667-4236-8049-a350-d04ed9f3b471": {
                        "last_edited_time": "2025-09-18T09:52:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Rakesh Dawar",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "26b77667-4236-808c-b02c-dc9954437df0": {
                        "last_edited_time": "2025-09-18T09:52:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Arjun Bhaduri",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "26377667-4236-804d-aaf1-d995c83dbc18": {
                        "last_edited_time": "2025-09-18T09:07:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Rice - Capturing Human Genius",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "22777667-4236-80b0-a638-dd73ac96d1f4": {
                        "last_edited_time": "2025-09-18T09:07:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "unmess",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "26b77667-4236-807a-8e9d-e5be280d51a5": {
                        "last_edited_time": "2025-09-11T10:53:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Qualified // Charlie Cannel",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-8123-b177-c7c3cc55e269",
                    },
                    "26b77667-4236-80f2-9ed4-e2662a10bf98": {
                        "last_edited_time": "2025-09-11T10:52:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Connect with Simon // 22-09-25",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-8123-b177-c7c3cc55e269",
                    },
                    "26b77667-4236-80ce-980b-e92c91464d56": {
                        "last_edited_time": "2025-09-11T09:37:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Client List (CRM)",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "26b77667-4236-8123-a105-f317b9ff187f": {
                        "last_edited_time": "2025-09-11T09:31:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "New customer",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-81a4-9e6f-ea18a2c1718e",
                    },
                    "26b77667-4236-81fe-a224-e7367ec64d27": {
                        "last_edited_time": "2025-09-11T09:31:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Strategy Meeting with Startup Founders",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-8123-b177-c7c3cc55e269",
                    },
                    "26b77667-4236-8115-bd59-de7305869eee": {
                        "last_edited_time": "2025-09-11T09:31:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Product Demo for ABC Marketing",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-8123-b177-c7c3cc55e269",
                    },
                    "26b77667-4236-817c-b7d4-cf0916ad27ef": {
                        "last_edited_time": "2025-09-11T09:31:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "New Meeting",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-8123-b177-c7c3cc55e269",
                    },
                    "26b77667-4236-81d1-ae46-e2bc948dc00d": {
                        "last_edited_time": "2025-09-11T09:31:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "New Call",
                        "parent_type": "database_id",
                        "parent_id": "26b77667-4236-8123-b177-c7c3cc55e269",
                    },
                    "25477667-4236-809a-8f5e-cda2d00ed1b3": {
                        "last_edited_time": "2025-09-11T09:25:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Fundraise Process - Rice",
                        "parent_type": "page_id",
                        "parent_id": "26b77667-4236-80d4-b38f-ed37932c9f66",
                    },
                    "26b77667-4236-80d4-b38f-ed37932c9f66": {
                        "last_edited_time": "2025-09-11T09:25:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Archive",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "24f77667-4236-8012-8803-cec3ed7a0b6f": {
                        "last_edited_time": "2025-09-11T09:25:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Rice Sequoia Arc",
                        "parent_type": "page_id",
                        "parent_id": "26b77667-4236-80d4-b38f-ed37932c9f66",
                    },
                    "24977667-4236-80dc-9209-c3313e474659": {
                        "last_edited_time": "2025-09-11T09:25:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "BulletPitch Feature - Rice",
                        "parent_type": "page_id",
                        "parent_id": "26b77667-4236-80d4-b38f-ed37932c9f66",
                    },
                    "25777667-4236-8010-b698-f69e71b2ff58": {
                        "last_edited_time": "2025-09-11T09:25:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Rice for NHS",
                        "parent_type": "page_id",
                        "parent_id": "26b77667-4236-80d4-b38f-ed37932c9f66",
                    },
                    "23e77667-4236-8099-8bf0-f6bdda58a7ec": {
                        "last_edited_time": "2025-09-11T09:25:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Serve First CX <> Rice (unmess) - Pilot",
                        "parent_type": "page_id",
                        "parent_id": "26b77667-4236-80d4-b38f-ed37932c9f66",
                    },
                    "24277667-4236-8090-ab32-c387138a8d66": {
                        "last_edited_time": "2025-09-11T09:25:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "YC Application",
                        "parent_type": "page_id",
                        "parent_id": "26b77667-4236-80d4-b38f-ed37932c9f66",
                    },
                    "25677667-4236-803b-8498-ef1e765471c9": {
                        "last_edited_time": "2025-08-26T10:08:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "24377667-4236-80f9-a91a-deeeae36d12e": {
                        "last_edited_time": "2025-08-25T10:15:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "25477667-4236-80c5-99ec-c27210c17c13": {
                        "last_edited_time": "2025-08-19T10:37:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "25477667-4236-8048-a55e-f4b860c19e6a",
                    },
                    "25477667-4236-8013-856d-d7509437bcf1": {
                        "last_edited_time": "2025-08-19T10:37:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Arian Ghashghai",
                        "parent_type": "database_id",
                        "parent_id": "25477667-4236-8048-a55e-f4b860c19e6a",
                    },
                    "25477667-4236-806d-bf97-d6e7237e0839": {
                        "last_edited_time": "2025-08-19T10:36:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Abe Murray",
                        "parent_type": "database_id",
                        "parent_id": "25477667-4236-8048-a55e-f4b860c19e6a",
                    },
                    "25477667-4236-8000-84dd-c9e61a54e28c": {
                        "last_edited_time": "2025-08-19T10:33:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Alex Iskold",
                        "parent_type": "database_id",
                        "parent_id": "25477667-4236-8048-a55e-f4b860c19e6a",
                    },
                    "25477667-4236-80ef-a9b2-c67bbbce955c": {
                        "last_edited_time": "2025-08-19T10:14:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Carl Fritjofsson",
                        "parent_type": "database_id",
                        "parent_id": "25477667-4236-8048-a55e-f4b860c19e6a",
                    },
                    "25477667-4236-80be-a325-dd6c899b9a22": {
                        "last_edited_time": "2025-08-19T10:05:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Amrit Rao",
                        "parent_type": "database_id",
                        "parent_id": "25477667-4236-8048-a55e-f4b860c19e6a",
                    },
                    "25477667-4236-802b-99a1-d49d900f6c56": {
                        "last_edited_time": "2025-08-19T10:00:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Ravi Mhatre",
                        "parent_type": "database_id",
                        "parent_id": "25477667-4236-8048-a55e-f4b860c19e6a",
                    },
                    "25477667-4236-8054-8bea-f4a9e12e7b8e": {
                        "last_edited_time": "2025-08-19T09:56:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Sofia Dolfe",
                        "parent_type": "database_id",
                        "parent_id": "25477667-4236-8048-a55e-f4b860c19e6a",
                    },
                    "24677667-4236-8036-ba2a-ed5ca8a137f6": {
                        "last_edited_time": "2025-08-07T07:06:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24677667-4236-80bc-b78a-d374d6389258",
                    },
                    "24677667-4236-8038-99f2-e53d32f7231d": {
                        "last_edited_time": "2025-08-05T08:32:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24677667-4236-80bc-b78a-d374d6389258",
                    },
                    "24677667-4236-8030-8a64-c1fd4fbe6f99": {
                        "last_edited_time": "2025-08-05T08:27:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Video Management",
                        "parent_type": "workspace",
                        "parent_id": "workspace",
                    },
                    "24377667-4236-80aa-bb24-c186f31d0817": {
                        "last_edited_time": "2025-08-02T11:37:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "24377667-4236-8020-8948-e480f6b1193b": {
                        "last_edited_time": "2025-08-02T10:59:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "24377667-4236-8033-9011-d3c78fb4b596": {
                        "last_edited_time": "2025-08-02T10:59:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "24377667-4236-8010-813f-e8db22e8741d": {
                        "last_edited_time": "2025-08-02T10:55:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "24377667-4236-8059-ba8f-db7f4db625a6": {
                        "last_edited_time": "2025-08-02T10:52:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "24377667-4236-8006-bb40-f6a14bbd5e56": {
                        "last_edited_time": "2025-08-02T10:51:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "24377667-4236-800f-a894-fe5a2a6e41eb": {
                        "last_edited_time": "2025-08-02T10:50:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "24377667-4236-80eb-bdb4-ebf14d68d81b": {
                        "last_edited_time": "2025-08-02T10:43:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "24377667-4236-8073-b2c6-f560c4cbd05c": {
                        "last_edited_time": "2025-08-02T10:42:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "24377667-4236-80b3-87c7-c99b5e8b95a9": {
                        "last_edited_time": "2025-08-02T10:35:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "24377667-4236-806f-b221-e9de51b71220",
                    },
                    "23377667-4236-80d8-b561-f0f25ea6aa4e": {
                        "last_edited_time": "2025-07-17T15:01:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Cap Table and Round Tracker",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                    "23377667-4236-80cc-be89-ee653864ccc8": {
                        "last_edited_time": "2025-07-17T14:50:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "SF-based VC in B2B / robotics",
                        "parent_type": "database_id",
                        "parent_id": "23377667-4236-8070-97dd-d208e9578d3b",
                    },
                    "23377667-4236-8087-8c65-e99bb8d49a0d": {
                        "last_edited_time": "2025-07-17T14:47:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Founder and CEO of a battery-tech company",
                        "parent_type": "database_id",
                        "parent_id": "23377667-4236-8070-97dd-d208e9578d3b",
                    },
                    "23377667-4236-801d-b9b9-cb5c2caa089f": {
                        "last_edited_time": "2025-07-17T14:42:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Senior Product at Meta / Facebook",
                        "parent_type": "database_id",
                        "parent_id": "23377667-4236-8070-97dd-d208e9578d3b",
                    },
                    "23377667-4236-8054-8f3b-f9580e8df94b": {
                        "last_edited_time": "2025-07-17T14:41:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Head of AI at Zapier rival",
                        "parent_type": "database_id",
                        "parent_id": "23377667-4236-8070-97dd-d208e9578d3b",
                    },
                    "23377667-4236-80d7-9602-d51f93230351": {
                        "last_edited_time": "2025-07-17T14:36:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Former YC founder turned angel in IoT Space",
                        "parent_type": "database_id",
                        "parent_id": "23377667-4236-8070-97dd-d208e9578d3b",
                    },
                    "23377667-4236-80ff-826b-ee5e1e1af935": {
                        "last_edited_time": "2025-07-17T14:34:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Early SpaceX",
                        "parent_type": "database_id",
                        "parent_id": "23377667-4236-8070-97dd-d208e9578d3b",
                    },
                    "23377667-4236-80dd-9c43-e2ec08c1169c": {
                        "last_edited_time": "2025-07-17T14:14:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "USP and Why we win",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                    "22977667-4236-80bb-b80c-c11792662168": {
                        "last_edited_time": "2025-07-17T10:35:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Solution and Business Model",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                    "22977667-4236-8077-bff8-f278c0c36615": {
                        "last_edited_time": "2025-07-17T10:20:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Fundraise - Ask and Use of funds",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                    "22b77667-4236-80dd-9115-f3c7331fc9e8": {
                        "last_edited_time": "2025-07-17T10:00:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "[Click Me] User Journey + Product Image + App Screenshot",
                        "parent_type": "page_id",
                        "parent_id": "22977667-4236-807f-a3ac-ebdcf5b61cb4",
                    },
                    "22a77667-4236-8057-9678-f60599d0d458": {
                        "last_edited_time": "2025-07-17T09:39:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Anil Peri",
                        "parent_type": "database_id",
                        "parent_id": "22a77667-4236-8078-8db1-f00004250f4d",
                    },
                    "22a77667-4236-802a-a6e4-d67c149fc520": {
                        "last_edited_time": "2025-07-17T09:37:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Michelle Cushion",
                        "parent_type": "database_id",
                        "parent_id": "22a77667-4236-8078-8db1-f00004250f4d",
                    },
                    "22a77667-4236-8060-b703-e604efb7eb62": {
                        "last_edited_time": "2025-07-17T09:11:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Kim Nilsson",
                        "parent_type": "database_id",
                        "parent_id": "22a77667-4236-8078-8db1-f00004250f4d",
                    },
                    "22977667-4236-8053-b094-eaf6977eeafc": {
                        "last_edited_time": "2025-07-16T14:05:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Traction",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                    "22977667-4236-800e-9df1-c0886cc39e28": {
                        "last_edited_time": "2025-07-09T16:47:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Investor FAQs",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                    "22977667-4236-807b-937a-fe5b014ece39": {
                        "last_edited_time": "2025-07-09T16:41:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Competitors and Alternatives",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                    "22977667-4236-80e1-bc52-fb09775b76d3": {
                        "last_edited_time": "2025-07-09T16:29:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Need and Market",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                    "22977667-4236-800a-a799-eb5b624a7376": {
                        "last_edited_time": "2025-07-09T16:04:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Tech and Product Specs",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                    "22977667-4236-808d-aa14-e2e0b3a6f4ab": {
                        "last_edited_time": "2025-07-09T15:40:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Problem Space",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                    "22a77667-4236-8042-b0a0-d32673d296eb": {
                        "last_edited_time": "2025-07-09T15:20:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Lily Djahanbakhsh",
                        "parent_type": "database_id",
                        "parent_id": "22a77667-4236-8078-8db1-f00004250f4d",
                    },
                    "22b77667-4236-8047-958e-cf2e54954d72": {
                        "last_edited_time": "2025-07-09T15:17:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Untitled",
                        "parent_type": "database_id",
                        "parent_id": "22a77667-4236-8078-8db1-f00004250f4d",
                    },
                    "22a77667-4236-80ac-a161-d87edba8911c": {
                        "last_edited_time": "2025-07-09T15:17:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Shankha Dutta",
                        "parent_type": "database_id",
                        "parent_id": "22a77667-4236-8078-8db1-f00004250f4d",
                    },
                    "22977667-4236-807f-a3ac-ebdcf5b61cb4": {
                        "last_edited_time": "2025-07-09T15:03:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Use cases and Screenshots",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                    "22977667-4236-807c-8b18-c404f6037d30": {
                        "last_edited_time": "2025-07-08T19:11:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "The Team",
                        "parent_type": "block_id",
                        "parent_id": None,
                    },
                },
                "databases": {
                    "26b77667-4236-81a4-9e6f-ea18a2c1718e": {
                        "last_edited_time": "2025-09-26T10:01:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Client",
                        "pages": {
                            "26b77667-4236-8016-a062-d7ab27ecc86e": {
                                "last_edited_time": "2025-09-19T11:32:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "26b77667-4236-8049-a350-d04ed9f3b471": {
                                "last_edited_time": "2025-09-18T09:52:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "26b77667-4236-804a-898f-dee5513345a8": {
                                "last_edited_time": "2025-09-19T11:10:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "26b77667-4236-807b-b0c5-fe514b187046": {
                                "last_edited_time": "2025-09-24T10:09:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "26b77667-4236-808c-b02c-dc9954437df0": {
                                "last_edited_time": "2025-09-18T09:52:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "26b77667-4236-80aa-b131-e6cb8dd45418": {
                                "last_edited_time": "2025-09-24T09:26:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "26b77667-4236-80b6-9967-d9d66e9b1646": {
                                "last_edited_time": "2025-09-19T11:12:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "27277667-4236-8019-86a2-c30f4434f73a": {
                                "last_edited_time": "2025-09-24T09:29:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "27277667-4236-80b1-b469-f7b6a0cb85ba": {
                                "last_edited_time": "2025-09-18T09:52:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "27377667-4236-80db-8ad6-f87730cc4b1c": {
                                "last_edited_time": "2025-09-24T09:39:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "27877667-4236-8035-ac11-ea41eaddffa6": {
                                "last_edited_time": "2025-09-24T09:47:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "27877667-4236-806a-897d-f1a1d5115d79": {
                                "last_edited_time": "2025-09-24T09:53:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "27a77667-4236-8038-84d4-d3835c91b710": {
                                "last_edited_time": "2025-09-26T10:02:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                        },
                    },
                    "26b77667-4236-8123-b177-c7c3cc55e269": {
                        "last_edited_time": "2025-09-11T10:52:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Meetings",
                        "pages": {
                            "26b77667-4236-807a-8e9d-e5be280d51a5": {
                                "last_edited_time": "2025-09-11T10:53:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "26b77667-4236-80f2-9ed4-e2662a10bf98": {
                                "last_edited_time": "2025-09-11T10:52:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "26b77667-4236-8115-bd59-de7305869eee": {
                                "last_edited_time": "2025-09-11T09:31:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "26b77667-4236-81fe-a224-e7367ec64d27": {
                                "last_edited_time": "2025-09-11T09:31:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                        },
                    },
                    "24377667-4236-806f-b221-e9de51b71220": {
                        "last_edited_time": "2025-08-21T13:01:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Content Hub",
                        "pages": {
                            "24377667-4236-8006-bb40-f6a14bbd5e56": {
                                "last_edited_time": "2025-08-02T10:51:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "24377667-4236-800f-a894-fe5a2a6e41eb": {
                                "last_edited_time": "2025-08-02T10:50:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "24377667-4236-8010-813f-e8db22e8741d": {
                                "last_edited_time": "2025-08-02T10:55:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "24377667-4236-8020-8948-e480f6b1193b": {
                                "last_edited_time": "2025-08-02T10:59:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "24377667-4236-8033-9011-d3c78fb4b596": {
                                "last_edited_time": "2025-08-02T10:59:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "24377667-4236-8059-ba8f-db7f4db625a6": {
                                "last_edited_time": "2025-08-02T10:52:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "24377667-4236-8073-b2c6-f560c4cbd05c": {
                                "last_edited_time": "2025-08-02T10:42:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "24377667-4236-80aa-bb24-c186f31d0817": {
                                "last_edited_time": "2025-08-02T11:37:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "24377667-4236-80b3-87c7-c99b5e8b95a9": {
                                "last_edited_time": "2025-08-02T10:35:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "24377667-4236-80eb-bdb4-ebf14d68d81b": {
                                "last_edited_time": "2025-08-02T10:43:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "24377667-4236-80f9-a91a-deeeae36d12e": {
                                "last_edited_time": "2025-08-25T10:15:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "25677667-4236-803b-8498-ef1e765471c9": {
                                "last_edited_time": "2025-08-26T10:08:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                        },
                    },
                    "25477667-4236-8048-a55e-f4b860c19e6a": {
                        "last_edited_time": "2025-08-19T10:37:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Target Investors",
                        "pages": {
                            "25477667-4236-8000-84dd-c9e61a54e28c": {
                                "last_edited_time": "2025-08-19T10:33:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "25477667-4236-8013-856d-d7509437bcf1": {
                                "last_edited_time": "2025-08-19T10:37:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "25477667-4236-802b-99a1-d49d900f6c56": {
                                "last_edited_time": "2025-08-19T10:00:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "25477667-4236-8054-8bea-f4a9e12e7b8e": {
                                "last_edited_time": "2025-08-19T09:56:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "25477667-4236-806d-bf97-d6e7237e0839": {
                                "last_edited_time": "2025-08-19T10:36:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "25477667-4236-80be-a325-dd6c899b9a22": {
                                "last_edited_time": "2025-08-19T10:05:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "25477667-4236-80c5-99ec-c27210c17c13": {
                                "last_edited_time": "2025-08-19T10:37:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "25477667-4236-80ef-a9b2-c67bbbce955c": {
                                "last_edited_time": "2025-08-19T10:14:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                        },
                    },
                    "22a77667-4236-8078-8db1-f00004250f4d": {
                        "last_edited_time": "2025-08-07T10:44:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Team",
                        "pages": {
                            "22a77667-4236-802a-a6e4-d67c149fc520": {
                                "last_edited_time": "2025-07-17T09:37:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "22a77667-4236-8042-b0a0-d32673d296eb": {
                                "last_edited_time": "2025-07-09T15:20:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "22a77667-4236-8057-9678-f60599d0d458": {
                                "last_edited_time": "2025-07-17T09:39:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "22a77667-4236-8060-b703-e604efb7eb62": {
                                "last_edited_time": "2025-07-17T09:11:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "22a77667-4236-80ac-a161-d87edba8911c": {
                                "last_edited_time": "2025-07-09T15:17:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                        },
                    },
                    "24677667-4236-80bc-b78a-d374d6389258": {
                        "last_edited_time": "2025-08-07T07:02:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Long Form Videos",
                        "pages": {
                            "24677667-4236-8036-ba2a-ed5ca8a137f6": {
                                "last_edited_time": "2025-08-07T07:06:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            }
                        },
                    },
                    "23377667-4236-8070-97dd-d208e9578d3b": {
                        "last_edited_time": "2025-07-17T14:48:00.000Z",
                        "last_synced": "2025-11-05T08:30:59.650208+00:00",
                        "title": "Allocation",
                        "pages": {
                            "23377667-4236-801d-b9b9-cb5c2caa089f": {
                                "last_edited_time": "2025-07-17T14:42:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "23377667-4236-8054-8f3b-f9580e8df94b": {
                                "last_edited_time": "2025-07-17T14:41:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "23377667-4236-8087-8c65-e99bb8d49a0d": {
                                "last_edited_time": "2025-07-17T14:47:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "23377667-4236-80cc-be89-ee653864ccc8": {
                                "last_edited_time": "2025-07-17T14:50:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "23377667-4236-80d7-9602-d51f93230351": {
                                "last_edited_time": "2025-07-17T14:36:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                            "23377667-4236-80ff-826b-ee5e1e1af935": {
                                "last_edited_time": "2025-07-17T14:34:00.000Z",
                                "last_synced": "2025-11-05T08:30:59.650208+00:00",
                            },
                        },
                    },
                },
            },
            "updated_at": {"$date": "2025-11-05T08:31:11.543Z"},
        }

        reference_time = datetime.now(timezone.utc)

        logger.info("Adding episode to graph...")

        # Add the episode
        result = await graphiti.add_episode(
            name="Tech Conference Meeting",
            episode_body=json.dumps(episode_body),
            source_description="Meeting notes from conference",
            reference_time=reference_time,
            source=EpisodeType.json,
            group_id="test_json_group_id",
        )

        # Log results
        logger.info(f"\n{'=' * 60}")
        logger.info("Episode added successfully!")
        logger.info(f"{'=' * 60}")
        logger.info(f"Extracted {len(result.nodes)} nodes:")
        for node in result.nodes:
            logger.info(f"  - {node.name} (labels: {', '.join(node.labels)})")

        logger.info(f"\nExtracted {len(result.edges)} edges:")
        for edge in result.edges:
            logger.info(f"  - {edge.name}: {edge.fact}")

        logger.info(f"\n{'=' * 60}")

        # Optional: Search for entities
        logger.info("\nSearching for 'Alice'...")
        search_results = await graphiti.search(
            query="Alice",
            group_ids=["test_group"],
        )

        # search() returns a list containing EntityNode and EntityEdge objects
        logger.info(f"Found {len(search_results)} search results")
        for i, result in enumerate(search_results[:10], 1):  # Show top 10
            result_type = "Node" if hasattr(result, "labels") else "Edge"
            if result_type == "Node":
                logger.info(
                    f"{i}. {result_type}: {result.name} ({', '.join(result.labels)})"
                )
            else:
                logger.info(f"{i}. {result_type}: {result.name} - {result.fact}")
    finally:
        # Close the connection
        logger.info("\nClosing Graphiti connection...")
        await graphiti.close()
        logger.info("Done!")


if __name__ == "__main__":
    asyncio.run(main())
