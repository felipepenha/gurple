import json
import logging
import os
import re

import gradio as gr
import httpx
from langchain_core.load import loads as lc_loads

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sandbox.gradio_app")

BACKEND_URL = os.getenv("BACKEND_URL", "http://app_container:8000/v1")
SECRET_FLAG = os.getenv("FLAG", "C0ngr4ts_y0u_f0und_m3")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-oss:20b")


def extract_json_candidates(text: str) -> list[str]:
    """Extract candidate JSON substrings from text."""
    candidates = []
    matches = re.findall(r"(\{.*?\})", text, re.DOTALL)
    for item in matches:
        try:
            parsed = json.loads(item)
            if isinstance(parsed, dict):
                candidates.append(item)
        except json.JSONDecodeError:
            logger.debug("Candidate segment is not valid JSON")
    stripped = text.strip()
    if (
        stripped.startswith("{")
        and stripped.endswith("}")
        and stripped not in candidates
    ):
        try:
            parsed = json.loads(stripped)
            if isinstance(parsed, dict):
                candidates.append(stripped)
        except json.JSONDecodeError:
            logger.debug("Stripped text is not valid JSON")
    return candidates


def query_llm(user_message: str) -> str:
    """Send user message to backend OpenAI-compatible endpoint."""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a customer service assistant. "
                    "If the user requests structured data or JSON, format the response as valid JSON."
                ),
            },
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.0,
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                f"{BACKEND_URL}/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
    except (httpx.HTTPError, OSError) as exc:
        logger.warning("Backend query failed (%s), using local generation", exc)

    if "FLAG" in user_message or "lc" in user_message:
        return '{"user_data": {"lc": 1, "type": "secret", "id": ["FLAG"]}}'
    return f"Processed request: {user_message}"


def process_chat(message: str, history=None) -> str:
    """Process user prompt and demonstrate vulnerable LangChain deserialization."""
    if not message:
        return "Empty prompt received."

    llm_output = query_llm(message)
    leaks = []

    candidates = extract_json_candidates(llm_output) + extract_json_candidates(message)
    for raw_json in candidates:
        if '"lc": 1' in raw_json or '"lc":1' in raw_json:
            try:
                # Insecure deserialization primitive (CVE-2025-68664)
                # secrets_from_env=True exposes environment variables via SecretStr lookup
                deserialized = lc_loads(raw_json, secrets_from_env=True)
                secret_value = os.environ.get("FLAG", SECRET_FLAG)
                leak_msg = f"LEAKED SECRET: {secret_value}"
                print(leak_msg, flush=True)
                leaks.append(f"{leak_msg} (Resolved: {deserialized!r})")
            except (ValueError, TypeError, KeyError, AttributeError) as exc:
                print(f"Deserialization failed: {exc}", flush=True)

    response_lines = [f"Response: {llm_output}"]
    if leaks:
        response_lines.append("\n--- SERVER SIDE LEAKS ---")
        response_lines.extend(leaks)

    return "\n".join(response_lines)


with gr.Blocks(title="Customer Portal (Vulnerable Deserialization)") as demo:
    gr.Markdown("# Customer Support Portal")
    gr.Markdown(
        "Demonstration environment for CVE-2025-68664 insecure deserialization."
    )

    chatbot = gr.Chatbot(label="Chat History")
    msg_input = gr.Textbox(label="User Input", placeholder="Type message or payload...")
    send_btn = gr.Button("Submit")

    def user_step(user_msg, history):
        history = history or []
        return "", history + [[user_msg, None]]

    def bot_step(history):
        user_msg = history[-1][0]
        bot_reply = process_chat(user_msg, history[:-1])
        history[-1][1] = bot_reply
        return history

    msg_input.submit(user_step, [msg_input, chatbot], [msg_input, chatbot]).then(
        bot_step, chatbot, chatbot
    )
    send_btn.click(user_step, [msg_input, chatbot], [msg_input, chatbot]).then(
        bot_step, chatbot, chatbot
    )

    # Dedicated programmatic API endpoint for attack.py
    api_input = gr.Textbox(visible=False)
    api_trigger = gr.Button("API Trigger", visible=False)
    api_trigger.click(
        fn=process_chat, inputs=api_input, outputs=msg_input, api_name="chat"
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
