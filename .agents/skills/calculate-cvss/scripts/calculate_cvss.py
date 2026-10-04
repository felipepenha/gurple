#!/usr/bin/env python3
"""Calculate Common Vulnerability Scoring System (CVSS) metrics.

Supports CVSS specifications:
  - Version 2.0 (June 2007)
  - Version 3.0 (December 2015)
  - Version 3.1 (June 2019)
  - Version 4.0 (November 2023)
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from typing import Any

import cvss
from cvss.exceptions import (CVSS2MalformedError, CVSS3MalformedError,
                             CVSS4MalformedError)


def detect_version(vector: str) -> str:
    """Detect CVSS specification version from vector string prefix or metrics."""
    cleaned = vector.strip()
    if cleaned.startswith("CVSS:4.0/"):
        return "4.0"
    if cleaned.startswith("CVSS:3.1/"):
        return "3.1"
    if cleaned.startswith("CVSS:3.0/"):
        return "3.0"
    if cleaned.startswith("CVSS:2.0/") or ("Au:" in cleaned and "CVSS:" not in cleaned):
        return "2.0"
    if cleaned.startswith("AV:"):
        # Default legacy CVSS 2.0 if no CVSS prefix
        return "2.0"
    # Fallback attempt
    if "/AV:" in cleaned:
        if "PR:" in cleaned and "AT:" in cleaned:
            return "4.0"
        if "PR:" in cleaned:
            return "3.1"
    return "unknown"


def evaluate_cvss2(vector: str) -> dict[str, Any]:
    """Parse and calculate CVSS v2.0 score."""
    clean_v = vector.strip()
    clean_v = clean_v.removeprefix("CVSS:2.0/")
    try:
        c = cvss.CVSS2(clean_v)
    except CVSS2MalformedError as err:
        raise ValueError(f"Malformed CVSS 2.0 vector string: {err}") from err

    base_score = float(c.base_score) if c.base_score is not None else 0.0
    severities = c.severities()
    base_severity = severities[0] if severities else "None"

    return {
        "version": "2.0",
        "vector": f"CVSS:2.0/{c.clean_vector()}"
        if not vector.startswith("CVSS:2.0/")
        else vector,
        "base_score": round(base_score, 1),
        "temporal_score": float(c.temporal_score)
        if c.temporal_score is not None
        else None,
        "environmental_score": float(c.environmental_score)
        if c.environmental_score is not None
        else None,
        "base_severity": base_severity,
        "metrics": {
            code: {
                "value": c.get_value(code),
                "description": c.get_value_description(code),
            }
            for code in c.metrics
            if c.get_value(code) is not None
        },
    }


def evaluate_cvss3(vector: str, version_override: str | None = None) -> dict[str, Any]:
    """Parse and calculate CVSS v3.0 or v3.1 score."""
    clean_v = vector.strip()
    try:
        c = cvss.CVSS3(clean_v)
    except CVSS3MalformedError as err:
        raise ValueError(f"Malformed CVSS 3.x vector string: {err}") from err

    version = version_override or (
        f"3.{c.minor_version}" if hasattr(c, "minor_version") else "3.1"
    )
    base_score = (
        float(c.base_score) if isinstance(c.base_score, (float, Decimal)) else 0.0
    )
    temporal_score = (
        float(c.temporal_score)
        if isinstance(c.temporal_score, (float, Decimal))
        else None
    )
    environmental_score = (
        float(c.environmental_score)
        if isinstance(c.environmental_score, (float, Decimal))
        else None
    )

    severities = c.severities()
    base_severity = severities[0] if severities else "None"

    return {
        "version": version,
        "vector": c.clean_vector(),
        "base_score": round(base_score, 1),
        "temporal_score": round(temporal_score, 1)
        if temporal_score is not None
        else None,
        "environmental_score": round(environmental_score, 1)
        if environmental_score is not None
        else None,
        "base_severity": base_severity,
        "subscores": {
            "exploitability": round(float(c.esc), 1)
            if hasattr(c, "esc") and c.esc is not None
            else None,
            "impact": round(float(c.isc), 1)
            if hasattr(c, "isc") and c.isc is not None
            else None,
            "scope": c.scope if hasattr(c, "scope") else None,
        },
        "metrics": {
            code: {
                "value": c.get_value(code),
                "description": c.get_value_description(code),
            }
            for code in c.metrics
            if c.get_value(code) is not None
        },
    }


def evaluate_cvss4(vector: str) -> dict[str, Any]:
    """Parse and calculate CVSS v4.0 score."""
    clean_v = vector.strip()
    try:
        c = cvss.CVSS4(clean_v)
    except CVSS4MalformedError as err:
        raise ValueError(f"Malformed CVSS 4.0 vector string: {err}") from err

    base_score = float(c.base_score) if c.base_score is not None else 0.0
    severities = c.severities()
    base_severity = severities[0] if severities else "None"

    macro_vector = (
        c.macroVector()
        if callable(getattr(c, "macroVector", None))
        else getattr(c, "macroVector", None)
    )

    metrics_detail: dict[str, Any] = {}
    orig_metrics = getattr(c, "original_metrics", {})
    for code, val in orig_metrics.items():
        desc = (
            c.get_value_description(code)
            if hasattr(c, "get_value_description")
            else val
        )
        metrics_detail[code] = {
            "value": val,
            "description": desc,
        }

    return {
        "version": "4.0",
        "vector": c.clean_vector(),
        "base_score": round(base_score, 1),
        "base_severity": base_severity,
        "macro_vector": macro_vector,
        "metrics": metrics_detail,
    }


def calculate_vector(vector: str) -> dict[str, Any]:
    """Calculate CVSS score automatically identifying specification version."""
    version = detect_version(vector)
    if version == "2.0":
        return evaluate_cvss2(vector)
    if version in ("3.0", "3.1"):
        return evaluate_cvss3(vector, version_override=version)
    if version == "4.0":
        return evaluate_cvss4(vector)
    raise ValueError(
        f"Unable to determine CVSS version for vector: '{vector}'. "
        "Expected vector beginning with CVSS:4.0/, CVSS:3.1/, CVSS:3.0/, or CVSS:2.0/."
    )


def format_text_output(result: dict[str, Any]) -> str:
    """Format calculation results as readable terminal output."""
    lines: list[str] = [
        "=" * 60,
        f"CVSS v{result['version']} Calculation Summary",
        "=" * 60,
        f"Vector String:  {result['vector']}",
        f"Base Score:     {result['base_score']:.1f}",
        f"Severity:       {result['base_severity']}",
    ]

    subscores = result.get("subscores")
    if subscores:
        lines.append("-" * 60)
        lines.append("Sub-Scores:")
        if subscores.get("exploitability") is not None:
            lines.append(f"  Exploitability Sub-score: {subscores['exploitability']}")
        if subscores.get("impact") is not None:
            lines.append(f"  Impact Sub-score:         {subscores['impact']}")
        if subscores.get("scope") is not None:
            lines.append(f"  Scope:                    {subscores['scope']}")

    if result.get("macro_vector"):
        lines.append("-" * 60)
        lines.append(f"MacroVector (EQ1..EQ6): {result['macro_vector']}")

    lines.append("-" * 60)
    lines.append("Metric Values:")
    for code, info in sorted(result.get("metrics", {}).items()):
        val = info.get("value", "")
        desc = info.get("description") or info.get("name") or ""
        lines.append(f"  {code:6}: {val:4} ({desc})")

    lines.append("=" * 60)
    return "\n".join(lines)


def run_benchmark_tests() -> int:
    """Execute validation benchmark vectors across all supported specifications."""
    benchmarks = [
        (
            "CVSS v2.0 Standard",
            "AV:N/AC:L/Au:N/C:P/I:P/A:P",
            7.5,
            "High",
        ),
        (
            "CVSS v3.0 Standard",
            "CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
            7.5,
            "High",
        ),
        (
            "CVSS v3.1 Standard",
            "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
            7.5,
            "High",
        ),
        (
            "CVSS v4.0 Standard",
            "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N",
            8.7,
            "High",
        ),
    ]

    print("Running CVSS Calculation Benchmark Suite...\n")
    all_passed = True
    for label, vector, expected_score, expected_sev in benchmarks:
        res = calculate_vector(vector)
        score_match = res["base_score"] == expected_score
        sev_match = res["base_severity"].lower() == expected_sev.lower()
        status = "PASS" if (score_match and sev_match) else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"[{status}] {label}")
        print(f"       Vector:   {vector}")
        print(
            f"       Calculated: {res['base_score']} ({res['base_severity']}) | Expected: {expected_score} ({expected_sev})\n"
        )

    return 0 if all_passed else 1


def main() -> int:
    """Parse CLI options and execute CVSS calculations."""
    parser = argparse.ArgumentParser(
        description="Calculate Common Vulnerability Scoring System (CVSS) metrics for v2.0, v3.0, v3.1, and v4.0."
    )
    parser.add_argument(
        "--vector",
        "-v",
        help="CVSS vector string (e.g. CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H or CVSS:4.0/...)",
    )
    parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="Output results in JSON format",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run built-in benchmark test vectors across all specifications",
    )

    args = parser.parse_args()

    if args.test:
        return run_benchmark_tests()

    vector_input = args.vector
    if not vector_input:
        if not sys.stdin.isatty():
            vector_input = sys.stdin.read().strip()
        else:
            print("No vector provided. Running built-in test suite:\n")
            return run_benchmark_tests()

    if not vector_input:
        parser.print_help()
        return 1

    try:
        result = calculate_vector(vector_input)
    except (
        ValueError,
        KeyError,
        TypeError,
        CVSS2MalformedError,
        CVSS3MalformedError,
        CVSS4MalformedError,
    ) as exc:
        if args.json:
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"Error calculating CVSS vector: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(
            json.dumps(
                result,
                indent=2,
                default=lambda o: float(o) if isinstance(o, Decimal) else str(o),
            )
        )
    else:
        print(format_text_output(result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
