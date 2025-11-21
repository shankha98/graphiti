"""
Search the Graphiti Kuzu database and display results.
Run with: uv run python search_graph.py
"""

import asyncio
import logging
from graphiti_core import Graphiti
from graphiti_core.driver.kuzu_driver import KuzuDriver

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def display_search_results(query: str, results: list, limit: int = 10):
    """Display search results in a formatted way."""
    print(f"\n{'=' * 80}")
    print(f"SEARCH QUERY: '{query}'")
    print(f"{'=' * 80}")
    print(f"Found {len(results)} results (showing top {min(len(results), limit)})\n")

    if not results:
        print("  No results found.")
        return

    for i, result in enumerate(results[:limit], 1):
        # Determine if it's a node or edge
        is_node = hasattr(result, "labels")

        print(f"{i}. ", end="")

        if is_node:
            # Display node
            labels = ", ".join(result.labels) if result.labels else "No labels"
            print(f"NODE: {result.name}")
            print(f"   Labels: {labels}")
            if hasattr(result, "summary") and result.summary:
                # Truncate long summaries
                summary = (
                    result.summary[:150] + "..."
                    if len(result.summary) > 150
                    else result.summary
                )
                print(f"   Summary: {summary}")
        else:
            # Display edge
            print(f"EDGE: {result.name}")
            # Truncate long facts
            fact = result.fact[:200] + "..." if len(result.fact) > 200 else result.fact
            print(f"   Fact: {fact}")
            if hasattr(result, "valid_at") and result.valid_at:
                print(f"   Valid from: {result.valid_at}")
            if hasattr(result, "invalid_at") and result.invalid_at:
                print(f"   Invalid from: {result.invalid_at}")
        print()


async def main():
    """Perform various searches on the Kuzu graph database."""

    # Same database path as test_kuzu_local.py
    kuzu_db_path = "./kuzu_test.db"

    logger.info(f"Connecting to Kuzu database at: {kuzu_db_path}")

    # Create Kuzu driver
    kuzu_driver = KuzuDriver(
        db=kuzu_db_path,
        max_concurrent_queries=1,
    )

    # Initialize Graphiti
    graphiti = Graphiti(graph_driver=kuzu_driver)

    try:
        # Define search queries to test
        searches = [
            ("Alice", ["test_group", "test_json_group_id"]),
            ("Bob", ["test_group"]),
            ("Google", ["test_group"]),
            ("conference", ["test_group"]),
            ("Techstars", ["test_json_group_id"]),
            ("fundraising", ["test_json_group_id"]),
        ]

        print("\n" + "=" * 80)
        print("GRAPHITI SEARCH DEMONSTRATION")
        print("=" * 80)
        print(f"Database: {kuzu_db_path}")
        print("=" * 80)

        for query, group_ids in searches:
            logger.info(f"Searching for: '{query}' in groups: {group_ids}")

            # Perform search
            results = await graphiti.search(
                query=query,
                group_ids=group_ids,
                num_results=10,
            )

            # Display results
            display_search_results(query, results, limit=10)

            # Small delay between searches for readability
            await asyncio.sleep(0.5)

        print("\n" + "=" * 80)
        print("Search demonstration complete!")
        print("=" * 80 + "\n")

    finally:
        await graphiti.close()
        logger.info("Connection closed.")


if __name__ == "__main__":
    asyncio.run(main())
