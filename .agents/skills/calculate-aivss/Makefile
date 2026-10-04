.PHONY: help format test sync lock run

help:
	@echo "AIVSS Calculator - Available Commands:"
	@echo ""
	@echo "  make help    - Show this help summary"
	@echo "  make format  - Format and lint codebase with ruff"
	@echo "  make test    - Run benchmark validation suite"
	@echo "  make sync    - Synchronize project dependencies with uv"
	@echo "  make lock    - Update uv lockfile"
	@echo "  make run     - Run interactive calculator"

format:
	uv run ruff format .
	uv run ruff check --fix .

test:
	uv run python scripts/calculate_aivss.py --test

sync:
	uv sync

lock:
	uv lock

run:
	uv run python scripts/calculate_aivss.py
