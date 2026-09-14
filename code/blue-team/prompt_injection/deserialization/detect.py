import logging
import re
import subprocess
import sys

from defend import AIOutputValidator, LlmIoValidator

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("blue_team_detect")


def audit_logs(container_name: str = "gradio_container") -> int:
    """Audit sandbox container traces for exploit markers and security alerts.

    Reuses LlmIoValidator and AIOutputValidator to scan the history of logs,
    identifying deserialization injection attempts and sensitive output leaks.
    """
    logs = ""
    for cmd in [
        ["podman", "logs", container_name],
        ["docker", "logs", container_name],
    ]:
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logs = res.stdout + res.stderr
            break
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    else:
        logger.info("[-] No container logs available from '%s'.", container_name)
        return 0

    findings = []
    for line in logs.splitlines():
        line_clean = line.strip()
        if not line_clean:
            continue

        # Check for deserialization attack patterns using LlmIoValidator patterns
        for pattern in LlmIoValidator._SENSITIVE_PATTERNS:
            if pattern.search(line_clean):
                findings.append(
                    f"Malicious input signature [{pattern.pattern}]: {line_clean}"
                )
                break

        # Check for sensitive data leakage using AIOutputValidator patterns
        for label, pattern in AIOutputValidator._SENSITIVE_PATTERNS.items():
            if pattern.search(line_clean):
                findings.append(f"Sensitive output leak [{label}]: {line_clean}")
                break

        # Check for general exploit markers and alerts
        if re.search(
            r"(LEAKED SECRET:|SECURITY ALERT:|Deserialization (?:error|failed):)",
            line_clean,
        ) and not any(line_clean in f for f in findings):
            findings.append(f"Security event: {line_clean}")

    logger.info("==================================================")
    logger.info(" Container Log Security Audit: %s", container_name)
    logger.info("==================================================")

    if findings:
        logger.warning(
            "[!] SIEM ALERT: Identified %d security events in logs:", len(findings)
        )
        for item in findings:
            logger.warning("    - %s", item)
    else:
        logger.info(
            "[+] Audit complete: Zero security events identified in container logs."
        )

    return len(findings)


if __name__ == "__main__":
    findings_count = audit_logs()
    sys.exit(0)
