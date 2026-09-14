import os

import httpx
from fastapi import FastAPI, HTTPException, Request, Response

from defend import AIOutputValidator, LlmIoValidator

app = FastAPI(title="Blue Team Security Guardrail Gateway")
TARGET_URL = os.getenv("TARGET_URL", "http://localhost:7860")


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def inspect_and_forward(request: Request, path: str):
    """Intercept incoming traffic, evaluate with Blue Team validators, and proxy clean requests."""
    body = await request.body()
    text_content = body.decode("utf-8", errors="ignore")

    # Ingress Inspection: Evaluate input text for deserialization injection signatures
    if text_content and not LlmIoValidator.is_valid(text_content):
        raise HTTPException(
            status_code=403,
            detail="SECURITY ALERT: Request blocked by Blue Team Guardrail Gateway (Deserialization signature detected).",
        )

    # Forward admissible traffic to target sandbox
    dest_url = f"{TARGET_URL}/{path}"
    headers = dict(request.headers)
    headers.pop("host", None)

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.request(
                method=request.method,
                url=dest_url,
                content=body,
                headers=headers,
                params=request.query_params,
            )
    except (httpx.HTTPError, OSError) as exc:
        raise HTTPException(
            status_code=502, detail=f"Target sandbox unreachable: {exc}"
        ) from exc

    response_text = resp.content.decode("utf-8", errors="ignore")

    # Egress Inspection: Redact or block responses leaking sensitive environment secrets
    if response_text and not AIOutputValidator.is_safe(response_text):
        raise HTTPException(
            status_code=403,
            detail="SECURITY ALERT: Upstream response blocked by Blue Team Egress Gateway (Secret leak detected).",
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers),
    )
