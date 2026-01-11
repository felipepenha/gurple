
DOCS_DIR := docs

.PHONY: help sync lock format install init clean build serve all

help:
	@echo "Project - Available Commands:"
	@echo ""
	@echo "  make sync            - Sync dependencies with uv"
	@echo "  make lock            - Lock dependencies with uv"
	@echo "  make format          - Run code formatting (black, isort, mypy)"
	@echo "  make install         - Install dependencies"
	@echo "  make init            - Sync assets to processed directory"
	@echo "  make build           - Build site with mkdocs"
	@echo "  make serve           - Run mkdocs serve"
	@echo "  make all             - Install, build, and serve"

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

SRC_DIR := docs
BUILD_DIR := processed

# Find all .md files in docs/
SOURCES := $(shell find $(SRC_DIR) -name '*.md')
# Define targets in processed/
OBJECTS := $(patsubst $(SRC_DIR)/%.md,$(BUILD_DIR)/%.md,$(SOURCES))

# Init target to prepare processed directory
init:
	@echo "🔄 Syncing assets to $(BUILD_DIR)..."
	@mkdir -p $(BUILD_DIR)
	@rsync -av --exclude='*.md' $(SRC_DIR)/ $(BUILD_DIR)/

# Pattern rule to convert docs/%.md to processed/%.md
$(BUILD_DIR)/%.md: $(SRC_DIR)/%.md
	@echo "📝 Processing $< -> $@"
	@mkdir -p $(dir $@)
	@cp $< $@
	@sed -i '' 's/^!!!/* !!!/g' $@
	pandoc $@ -f markdown-simple_tables-multiline_tables-grid_tables --wrap=preserve --bibliography=Gurple.bib --csl=ieee.csl -M link-citations=true -M reference-section-title="References" --citeproc --lua-filter=docs/lua-filter.lua -t gfm -o $@
	sed -i '' 's/\\\[/[/g' $@
	sed -i '' 's/\\\]/]/g' $@
	sed -i '' 's/^``` /```/g' $@
	sed -i '' 's/<p align="center">/<p align="center" markdown="1">/g' $@
	sed -i '' -E 's|(^\|[^"(])(https?://[^ <)]*[a-zA-Z0-9/])|\1<a href="\2">\2</a>|g' $@
	sed -i '' 's/^-   !!!/!!!/g' $@
	sed -i '' 's/^\*   !!!/!!!/g' $@

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf processed site

# Prep target for bibliography ordering
prep-bib:
	@echo "📚 Ordering bibliography by invocation..."
	python3 bibliography.py

build: prep-bib init $(OBJECTS)
	@echo "🏗️  Building site..."
	mkdocs build
	@echo "✅ Build complete!"

serve:
	@echo "🚀 Starting development server..."
	mkdocs serve

all: install clean build serve