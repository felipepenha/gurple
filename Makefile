
DOCS_DIR := docs

.PHONY: help serve build install sync lock format all

# Default target
help:
	@echo "Project - Available Commands:"
	@echo ""
	@echo "  make serve    - Run mkdocs serve"
	@echo "  make build    - Run mkdocs build"
	@echo "  make install  - Install dependencies"
	@echo "  make format   - Run code formatting (black, isort, mypy)"
	@echo "  make sync     - Sync dependencies with uv"
	@echo "  make lock     - Lock dependencies with uv"
	@echo ""
	@echo "Environment:"
	@echo "  - Docs Directory: $(DOCS_DIR)"
	@echo ""

sync:
	uv sync

lock:
	uv lock

format:
	uv run black .
	uv run isort .
	uv run mypy .

install:
	@echo "🚀 Installing dependencies..."
	pip install -r $(DOCS_DIR)/requirements.txt
	@echo "✅ Dependencies installed!"

serve:
	@echo "🚀 Starting development server..."
	mkdocs serve

build:
	@echo "🏗️  Building site..."
	mkdocs build
	@echo "✅ Build complete!"

all: install build serve
