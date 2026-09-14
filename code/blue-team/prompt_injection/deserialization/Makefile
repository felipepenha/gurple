.PHONY: all defend proxy detect test format sync lock

defend:
	uv run python defend.py

proxy:
	uv run uvicorn proxy:app --port 8080 --reload

detect:
	uv run python detect.py

test:
	uv run pytest test_defense.py -v

format:
	uv run ruff format .
	uv run ruff check --fix .

sync:
	uv sync --frozen

lock:
	uv lock

all: defend test format
