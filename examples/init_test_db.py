"""
Initialize the test Kuzu database if it doesn't exist.
Run with: uv run python examples/init_test_db.py
"""

import logging
from pathlib import Path

from graphiti_core.driver.kuzu_driver import KuzuDriver

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def init_test_db(db_path: str = "./kuzu_test.db"):
    """Initialize the test Kuzu database if it doesn't exist."""

    db_file = Path(db_path)

    # Check if database already exists
    if db_file.exists():
        logger.info(f"Database already exists at: {db_path}")
        logger.info(f"Database size: {db_file.stat().st_size / 1024:.2f} KB")
        return False

    logger.info(f"Creating new Kuzu database at: {db_path}")

    # Create the database by initializing a KuzuDriver
    # This will automatically create the database file and set up the schema
    driver = KuzuDriver(db=db_path, max_concurrent_queries=1)

    logger.info("✅ Database created successfully!")
    logger.info(f"Database file: {db_path}")
    logger.info("Schema initialized with tables:")
    logger.info("  - Entity (nodes)")
    logger.info("  - Episodic (nodes)")
    logger.info("  - Community (nodes)")
    logger.info("  - RelatesToNode_ (nodes)")
    logger.info("  - RELATES_TO (edges)")
    logger.info("  - MENTIONS (edges)")
    logger.info("  - HAS_MEMBER (edges)")

    # Close the driver (cleanup)
    # Note: KuzuDriver.close() doesn't actually close, relies on GC
    # but we call it anyway for API consistency
    import asyncio

    asyncio.run(driver.close())

    return True


if __name__ == "__main__":
    init_test_db()
