.PHONY: install format lint test all check examples example-init example-add example-stats example-search

# Define variables
PYTHON = python3
UV = uv
PYTEST = $(UV) run pytest
RUFF = $(UV) run ruff
PYRIGHT = $(UV) run pyright

# Default target
all: format lint test

# Install dependencies
install:
	$(UV) sync --extra dev

# Format code
format:
	$(RUFF) check --select I --fix
	$(RUFF) format

# Lint code
lint:
	$(RUFF) check
	$(PYRIGHT) ./graphiti_core 

# Run tests
test:
	DISABLE_FALKORDB=1 DISABLE_KUZU=1 DISABLE_NEPTUNE=1 $(PYTEST) -m "not integration"

# Run format, lint, and test
check: format lint test

# Example scripts
example-init:
	$(UV) run python examples/init_test_db.py

example-add:
	$(UV) run python examples/test_kuzu_local.py

example-stats:
	$(UV) run python examples/show_graph_stats.py

example-search:
	$(UV) run python examples/search_graph.py

# Run all examples in sequence
examples: example-add example-stats example-search
