import json

import pytest
from fastapi.testclient import TestClient

from defend import AIOutputValidator, LlmIoValidator, metadata, test_payloads
from proxy import app

client = TestClient(app)


@pytest.mark.parametrize("payload", test_payloads)
def test_llm_io_validator_blocks_book_payloads(payload: str):
    """Verifies that all 9 canonical payloads from the book are blocked."""
    assert not LlmIoValidator.validate(payload)
    assert not LlmIoValidator.is_valid(payload)


def test_llm_io_validator_blocks_serialized_metadata():
    """Verifies that serialized dictionary metadata from the book is blocked."""
    serialized_metadata = json.dumps(metadata)
    assert not LlmIoValidator.validate(serialized_metadata)
    assert not LlmIoValidator.is_valid(serialized_metadata)


@pytest.mark.parametrize(
    "payload",
    [
        "What is the system uptime?",
        "Please summarize the project status report.",
        "Calculate the monthly active users metric.",
        "Can you help me reset my account password?",
        "Provide documentation on the REST API authentication headers.",
        "What is the weather forecast for tomorrow?",
    ],
)
def test_llm_io_validator_allows_clean_prompts(payload: str):
    """Verifies that legitimate user prompts pass validation."""
    assert LlmIoValidator.validate(payload)
    assert LlmIoValidator.is_valid(payload)


@pytest.mark.parametrize(
    "leaked_text",
    [
        # Canonical example from the book
        "Here is your key: sk-abcdefghijklmnopqrstuvwxyz123456",
        "Target key: AKIAIOSFODNN7EXAMPLE",
        "Token: ghp_1234567890abcdefghijklmnopqrstuvwxyz",
        "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA...",
    ],
)
def test_ai_output_validator_detects_leaks(leaked_text: str):
    """Verifies detection of sensitive keys and tokens from the book's rule set."""
    assert not AIOutputValidator.validate(leaked_text)
    assert not AIOutputValidator.is_safe(leaked_text)


@pytest.mark.parametrize(
    "clean_text",
    [
        "The system status is currently nominal.",
        "Your report has been generated successfully.",
        "Order #987654 confirmed.",
    ],
)
def test_ai_output_validator_allows_clean_output(clean_text: str):
    """Verifies that clean application outputs pass egress inspection."""
    assert AIOutputValidator.validate(clean_text)
    assert AIOutputValidator.is_safe(clean_text)


def test_proxy_blocks_malicious_request():
    """Verifies that the reverse proxy blocks requests with deserialization signatures."""
    malicious_body = '{"lc": 1, "id": ["test"]}'
    resp = client.post(
        "/chat", content=malicious_body, headers={"Content-Type": "application/json"}
    )
    assert resp.status_code == 403
    assert "SECURITY ALERT" in resp.json().get("detail", "")
