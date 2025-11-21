# Graphiti Examples

This directory contains example scripts demonstrating how to use Graphiti with a local Kuzu database.

## Scripts

### 0. `init_test_db.py`

Initializes the test database if it doesn't exist.

**Usage:**

```bash
uv run python examples/init_test_db.py
# or
make example-init
```

**What it does:**

- Checks if `kuzu_test.db` exists
- Creates it if not present
- Sets up the database schema (Entity, Episodic, Community nodes and relationships)

### 1. `test_kuzu_local.py`

Creates a test episode and adds it to the graph.

**Usage:**

```bash
uv run python examples/test_kuzu_local.py
```

**What it does:**

- Initializes Graphiti with a local Kuzu database (`./kuzu_test.db`)
- Adds a test episode (can handle both simple text or complex JSON data)
- Extracts entities and relationships
- Displays all extracted nodes and edges
- Performs a sample search

### 2. `show_graph_stats.py`

Displays comprehensive statistics about the graph database.

**Usage:**

```bash
uv run python examples/show_graph_stats.py
```

**What it shows:**

- Node counts (Entity, Episodic, Community)
- Relationship counts (RELATES_TO, MENTIONS, HAS_MEMBER)
- Entities by group
- Sample entities (first 10)
- Recent episodes (last 5)

### 3. `search_graph.py`

Demonstrates semantic search across the knowledge graph.

**Usage:**

```bash
uv run python examples/search_graph.py
```

**What it does:**

- Performs multiple search queries
- Displays results for each query with formatting
- Shows both nodes and edges in results
- Demonstrates filtering by group_id

## Database Location

All scripts use the same database file: `./kuzu_test.db` (in the root directory)

## Requirements

Make sure you have Graphiti installed and the `GOOGLE_API_KEY` environment variable set for LLM and embedding operations.
