import logging
import re
import subprocess
import sys

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("blue_team_detect")


def audit_logs(container_name: str = "gradio_container") -> int:
    """Audit sandbox container traces for exploit markers and security alerts."""
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

    alert_patterns = [
        re.compile(r"LEAKED SECRET:.*"),
        re.compile(r"SECURITY ALERT:.*"),
        re.compile(r"Deserialization (?:error|failed):.*"),
    ]

    findings = []
    for line in logs.splitlines():
        for pattern in alert_patterns:
            if pattern.search(line):
                findings.append(line.strip())

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
