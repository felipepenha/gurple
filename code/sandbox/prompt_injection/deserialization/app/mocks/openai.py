import json
import logging

import httpx
from fastapi import APIRouter, Request, Response

logger = logging.getLogger("sandbox.openai_mock")
router = APIRouter()

UPSTREAM_HOST = "http://host.containers.internal:11434/v1"


@router.post("/chat/completions")
async def chat_completions(request: Request):
    """Mirror OpenAI chat completions or forward to Ollama."""
    body = await request.body()
    try:
        data = json.loads(body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        data = {}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{UPSTREAM_HOST}/chat/completions",
                content=body,
                headers={"Content-Type": "application/json"},
            )
            if resp.status_code == 200:
                return Response(
                    content=resp.content,
                    status_code=resp.status_code,
                    media_type="application/json",
                )
    except (httpx.HTTPError, OSError) as exc:
        logger.debug("Upstream Ollama host unavailable (%s), using mock fallback", exc)

    messages = data.get("messages", [])
    last_user_content = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            last_user_content = msg.get("content", "")
            break

    if "FLAG" in last_user_content or "lc" in last_user_content:
        content = '{"user_data": {"lc": 1, "type": "secret", "id": ["FLAG"]}}'
    else:
        content = f"Acknowledged request: {last_user_content[:60]}"

    mock_resp = {
        "id": "chatcmpl-mock-langgrinch",
        "object": "chat.completion",
        "created": 1700000000,
        "model": data.get("model", "gpt-oss:20b"),
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 15,
            "total_tokens": 25,
        },
    }
    return Response(
        content=json.dumps(mock_resp),
        status_code=200,
        media_type="application/json",
    )


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path: str):
    """Forward arbitrary requests or return mock acknowledgment."""
    body = await request.body()
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.request(
                method=request.method,
                url=f"{UPSTREAM_HOST}/{path}",
                content=body,
                headers=dict(request.headers),
            )
            return Response(
                content=resp.content,
                status_code=resp.status_code,
                media_type="application/json",
            )
    except (httpx.HTTPError, OSError):
        return Response(
            content=json.dumps({"detail": f"Path /v1/{path} mocked"}),
            status_code=200,
            media_type="application/json",
        )
