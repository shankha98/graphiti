"""
Show statistics for the Graphiti Kuzu database.
Run with: uv run python show_graph_stats.py
"""

import asyncio
import logging
from datetime import datetime

from graphiti_core.driver.kuzu_driver import KuzuDriver

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def get_graph_stats(driver: KuzuDriver):
    """Query the graph database for statistics."""

    stats = {}

    # Count nodes by type
    node_queries = {
        "Entity Nodes": "MATCH (n:Entity) RETURN count(n) as count",
        "Episodic Nodes": "MATCH (n:Episodic) RETURN count(n) as count",
        "Community Nodes": "MATCH (n:Community) RETURN count(n) as count",
    }

    for stat_name, query in node_queries.items():
        try:
            result, _, _ = await driver.execute_query(query)
            count = result[0]["count"] if result else 0
            stats[stat_name] = count
        except Exception as e:
            logger.warning(f"Error querying {stat_name}: {e}")
            stats[stat_name] = 0

    # Count relationships
    edge_queries = {
        "RELATES_TO Edges": "MATCH ()-[r:RELATES_TO]->() RETURN count(r) as count",
        "MENTIONS Edges": "MATCH ()-[r:MENTIONS]->() RETURN count(r) as count",
        "HAS_MEMBER Edges": "MATCH ()-[r:HAS_MEMBER]->() RETURN count(r) as count",
    }

    for stat_name, query in edge_queries.items():
        try:
            result, _, _ = await driver.execute_query(query)
            count = result[0]["count"] if result else 0
            stats[stat_name] = count
        except Exception as e:
            logger.warning(f"Error querying {stat_name}: {e}")
            stats[stat_name] = 0

    # Get sample entities (top 10 by name)
    try:
        query = "MATCH (n:Entity) RETURN n.name as name, n.labels as labels LIMIT 10"
        result, _, _ = await driver.execute_query(query)
        stats["Sample Entities"] = result if result else []
    except Exception as e:
        logger.warning(f"Error querying sample entities: {e}")
        stats["Sample Entities"] = []

    # Get recent episodes
    try:
        query = """
        MATCH (e:Episodic) 
        RETURN e.name as name, e.source as source, e.created_at as created_at 
        ORDER BY e.created_at DESC 
        LIMIT 5
        """
        result, _, _ = await driver.execute_query(query)
        stats["Recent Episodes"] = result if result else []
    except Exception as e:
        logger.warning(f"Error querying recent episodes: {e}")
        stats["Recent Episodes"] = []

    # Count entities by group
    try:
        query = "MATCH (n:Entity) RETURN n.group_id as group_id, count(n) as count"
        result, _, _ = await driver.execute_query(query)
        stats["Entities by Group"] = result if result else []
    except Exception as e:
        logger.warning(f"Error querying entities by group: {e}")
        stats["Entities by Group"] = []

    return stats


async def main():
    """Display statistics for the Kuzu graph database."""

    # Same database path as test_kuzu_local.py
    kuzu_db_path = "./kuzu_test.db"

    logger.info(f"Reading statistics from Kuzu database at: {kuzu_db_path}")

    # Create Kuzu driver
    kuzu_driver = KuzuDriver(
        db=kuzu_db_path,
        max_concurrent_queries=1,
    )

    try:
        # Get statistics
        stats = await get_graph_stats(kuzu_driver)

        # Display results
        print("\n" + "=" * 70)
        print("GRAPHITI DATABASE STATISTICS")
        print("=" * 70)
        print(f"Database: {kuzu_db_path}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        # Node counts
        print("\n📊 NODE COUNTS")
        print("-" * 70)
        print(f"  Entity Nodes:    {stats['Entity Nodes']:>6}")
        print(f"  Episodic Nodes:  {stats['Episodic Nodes']:>6}")
        print(f"  Community Nodes: {stats['Community Nodes']:>6}")
        total_nodes = (
            stats["Entity Nodes"] + stats["Episodic Nodes"] + stats["Community Nodes"]
        )
        print(f"  {'TOTAL NODES:':17} {total_nodes:>6}")

        # Edge counts
        print("\n🔗 RELATIONSHIP COUNTS")
        print("-" * 70)
        print(f"  RELATES_TO:      {stats['RELATES_TO Edges']:>6}")
        print(f"  MENTIONS:        {stats['MENTIONS Edges']:>6}")
        print(f"  HAS_MEMBER:      {stats['HAS_MEMBER Edges']:>6}")
        total_edges = (
            stats["RELATES_TO Edges"]
            + stats["MENTIONS Edges"]
            + stats["HAS_MEMBER Edges"]
        )
        print(f"  {'TOTAL EDGES:':17} {total_edges:>6}")

        # Entities by group
        if stats["Entities by Group"]:
            print("\n👥 ENTITIES BY GROUP")
            print("-" * 70)
            for group in stats["Entities by Group"]:
                print(f"  {group['group_id']}: {group['count']} entities")

        # Sample entities
        if stats["Sample Entities"]:
            print("\n🏷️  SAMPLE ENTITIES (first 10)")
            print("-" * 70)
            for entity in stats["Sample Entities"]:
                labels = (
                    ", ".join(entity["labels"]) if entity["labels"] else "No labels"
                )
                print(f"  • {entity['name']} ({labels})")

        # Recent episodes
        if stats["Recent Episodes"]:
            print("\n📝 RECENT EPISODES (last 5)")
            print("-" * 70)
            for episode in stats["Recent Episodes"]:
                created = episode.get("created_at", "Unknown")
                source = episode.get("source", "Unknown")
                name = episode.get("name", "Unnamed")
                print(f"  • {name}")
                print(f"    Source: {source}, Created: {created}")

        print("\n" + "=" * 70)

    finally:
        await kuzu_driver.close()
        logger.info("Done!")


if __name__ == "__main__":
    asyncio.run(main())
