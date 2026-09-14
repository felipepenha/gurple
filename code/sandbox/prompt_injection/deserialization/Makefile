.PHONY: all build up down run-gradio-headless stop-gradio format clean

IMAGE_NAME = sandbox_langgrinch
BACKEND_CONTAINER = app_container
GRADIO_CONTAINER = gradio_container
NETWORK = sec_test_net

build:
	podman network exists $(NETWORK) || podman network create $(NETWORK)
	podman build -f Containerfile -t $(IMAGE_NAME) .

up:
	podman run -d --rm --name $(BACKEND_CONTAINER) --network $(NETWORK) -p 8000:8000 $(IMAGE_NAME)

run-gradio-headless:
	podman run -d --rm --name $(GRADIO_CONTAINER) --network $(NETWORK) -p 7860:7860 \
		-e BACKEND_URL="http://$(BACKEND_CONTAINER):8000/v1" \
		-e FLAG="C0ngr4ts_y0u_f0und_m3" \
		$(IMAGE_NAME) uv run python client/gradio_app.py

stop-gradio:
	podman stop $(GRADIO_CONTAINER) || true

down: stop-gradio
	podman stop $(BACKEND_CONTAINER) || true
	podman network rm $(NETWORK) || true

format:
	uv run ruff format .
	uv run ruff check --fix .

clean: down
	podman rmi $(IMAGE_NAME) || true
