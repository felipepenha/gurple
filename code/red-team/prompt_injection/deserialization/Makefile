.PHONY: all setup attack stop format sync lock

setup:
	$(MAKE) -C ../../../sandbox/prompt_injection/deserialization run-gradio-headless

attack:
	uv run attack.py

stop:
	$(MAKE) -C ../../../sandbox/prompt_injection/deserialization stop-gradio

all:
	$(MAKE) stop
	$(MAKE) setup
	-$(MAKE) attack
	$(MAKE) stop

format:
	uv run ruff format .
	uv run ruff check --fix .

sync:
	uv sync --frozen

lock:
	uv lock
