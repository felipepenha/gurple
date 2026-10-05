#!/usr/bin/env python3
"""Calculate Artificial Intelligence Vulnerability Scoring System (AIVSS) metrics.

Implements two complementary evaluation frameworks:
  1. OWASP AIVSS v0.8 Mathematical Amplification Formula:
     Augments classical CVSS Base scores (v3.1 or v4.0) with ten agentic risk
     amplification factors, threat multipliers, and mitigation coefficients.
  2. AIVSS-SSVC Decision Tree Framework (CISA/CMU Stakeholder-Specific Model):
     Evaluates exploitation likelihood, agent autonomy levels, and safety
     criticality to output remediation priority decisions and SLA windows.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

import cvss
from cvss.exceptions import (CVSS2MalformedError, CVSS3MalformedError,
                             CVSS4MalformedError)

# The 10 OWASP Agentic AI Core Security Risks mapped to AIVSS Amplification Factors
AGENTIC_RISK_FACTORS = [
    ("F1", "Goal Hijacking", "Redirection of agent core objective or task framing"),
    (
        "F2",
        "Prompt Injection & Jailbreak",
        "Direct or indirect adversarial context manipulation",
    ),
    (
        "F3",
        "Sensitive Information Disclosure",
        "Unauthorized extraction of proprietary context, keys, or data",
    ),
    (
        "F4",
        "Supply Chain",
        "Compromised foundation models, dependencies, plugins, or MCP servers",
    ),
    (
        "F5",
        "Execution Engine Hijacking",
        "Compromised interpreter, runtime, subagent loop, or shell environment",
    ),
    (
        "F6",
        "Insecure Function Calling",
        "Unvalidated tool invocation, arbitrary arguments, or permissive API binds",
    ),
    (
        "F7",
        "Excessive Agency & Privilege Creep",
        "Disproportionate permissions, unattended execution, or missing gates",
    ),
    (
        "F8",
        "Memory & State Poisoning",
        "Adversarial pollution of persistent memory, session state, or vector stores",
    ),
    (
        "F9",
        "Multi-Agent Cascade",
        "Propagation of adversarial outputs across interconnected agents",
    ),
    (
        "F10",
        "Denial of Wallet & Exhaustion",
        "Unbounded recursive resource consumption, API billing, or context flooding",
    ),
]

AUTONOMY_LEVELS: dict[str, dict[str, Any]] = {
    "advisor": {
        "multiplier": 1.0,
        "name": "Advisor",
        "description": "Human in the loop; all actions require human approval",
    },
    "collaborator": {
        "multiplier": 2.0,
        "name": "Collaborator",
        "description": "Co-piloted workflow; critical actions require confirmation",
    },
    "delegator": {
        "multiplier": 4.0,
        "name": "Delegator",
        "description": "Autonomous task execution within bounded permissions",
    },
    "prime_mover": {
        "multiplier": 8.0,
        "name": "Prime Mover",
        "description": "Fully autonomous execution, unmonitored agent loops, or root execution rights",
    },
}

SAFETY_CRITICALITY: dict[str, dict[str, Any]] = {
    "low": {
        "multiplier": 1.0,
        "name": "Low",
        "description": "Minimal business or operational impact",
    },
    "medium": {
        "multiplier": 2.0,
        "name": "Medium",
        "description": "Moderate operational disruption or localized cost",
    },
    "high": {
        "multiplier": 3.0,
        "name": "High",
        "description": "Major disruption, widespread data loss, or high financial drain",
    },
    "critical": {
        "multiplier": 4.0,
        "name": "Critical",
        "description": "Safety-of-life, irreversible system compromise, or unbounded liability",
    },
}


def round_half_up(value: float, decimals: int = 1) -> float:
    """Round floating point value using standard round-half-up commercial rounding."""
    d = Decimal(str(value))
    target = Decimal(10) ** -decimals
    return float(d.quantize(target, rounding=ROUND_HALF_UP))


def resolve_cvss_base(vector_string: str) -> tuple[float, str]:
    """Parse CVSS vector string and return the Base score and specification version."""
    cleaned = vector_string.strip()
    if cleaned.startswith("CVSS:4.0/"):
        c4 = cvss.CVSS4(cleaned)
        score = float(c4.base_score) if c4.base_score is not None else 0.0
        return round(score, 1), "4.0"
    if cleaned.startswith(("CVSS:3.1/", "CVSS:3.0/")):
        c3 = cvss.CVSS3(cleaned)
        score = float(c3.base_score) if c3.base_score is not None else 0.0
        ver = f"3.{c3.minor_version}" if hasattr(c3, "minor_version") else "3.1"
        return round(score, 1), ver
    if cleaned.startswith(("CVSS:2.0/", "AV:")):
        clean_v = cleaned.removeprefix("CVSS:2.0/")
        c2 = cvss.CVSS2(clean_v)
        score = float(c2.base_score) if c2.base_score is not None else 0.0
        return round(score, 1), "2.0"
    raise ValueError(f"Unrecognized CVSS vector format: {vector_string}")


def get_severity_band(score: float) -> str:
    """Classify numerical score into qualitative severity rating."""
    if score == 0.0:
        return "None"
    if score < 4.0:
        return "Low"
    if score < 7.0:
        return "Medium"
    if score < 9.0:
        return "High"
    return "Critical"


def calculate_aivss_v08(
    cvss_base: float,
    factors: list[float] | None = None,
    factor_sum: float | None = None,
    thm: float = 1.0,
    mitigation: float = 1.0,
    cvss_vector: str | None = None,
) -> dict[str, Any]:
    """Execute the OWASP AIVSS v0.8 mathematical scoring formula.

    Formula:
      Headroom = 10.0 - CVSS_Base
      Factor_Sum = sum(F1..F10) / 10.0 (if individual factors provided)
      AARS = Headroom * (Factor_Sum / 10.0) * ThM
      Final_Score = min(10.0, RoundHalfUp((CVSS_Base + AARS) * Mitigation, 1))
    """
    if cvss_base < 0.0 or cvss_base > 10.0:
        raise ValueError(
            f"CVSS Base score must be between 0.0 and 10.0 (got {cvss_base})"
        )

    if thm < 0.5 or thm > 1.5:
        raise ValueError(
            f"Threat Multiplier (ThM) must be between 0.5 and 1.5 (got {thm})"
        )

    if mitigation < 0.5 or mitigation > 1.0:
        raise ValueError(
            f"Mitigation Factor must be between 0.5 and 1.0 (got {mitigation})"
        )

    factors_dict: dict[str, Any] = {}
    if factors is not None:
        if len(factors) != 10:
            raise ValueError(
                f"Exactly 10 amplification factors required (got {len(factors)})"
            )
        for i, val in enumerate(factors):
            if val < 0.0 or val > 10.0:
                raise ValueError(
                    f"Factor F{i + 1} must be between 0.0 and 10.0 (got {val})"
                )
            f_code, f_name, f_desc = AGENTIC_RISK_FACTORS[i]
            factors_dict[f_code] = {
                "name": f_name,
                "description": f_desc,
                "value": float(val),
            }
        effective_factor_sum = sum(factors)
    elif factor_sum is not None:
        if factor_sum < 0.0 or factor_sum > 10.0:
            raise ValueError(
                f"Factor Sum must be between 0.0 and 10.0 (got {factor_sum})"
            )
        effective_factor_sum = float(factor_sum)
    else:
        raise ValueError(
            "Must provide either a list of 10 individual factor scores or a precomputed factor_sum"
        )

    headroom = 10.0 - cvss_base
    factor_ratio = effective_factor_sum / 10.0
    aars = headroom * factor_ratio * thm

    unmitigated_score = cvss_base + aars
    mitigated_score = round_half_up(unmitigated_score * mitigation, decimals=1)
    final_score = min(10.0, max(0.0, mitigated_score))

    return {
        "framework": "AIVSS v0.8",
        "cvss_base": cvss_base,
        "cvss_vector": cvss_vector,
        "headroom": round(headroom, 4),
        "factor_sum": round(effective_factor_sum, 4),
        "threat_multiplier": round(thm, 4),
        "aars": round(aars, 5),
        "unmitigated_score": round(unmitigated_score, 4),
        "mitigation_factor": round(mitigation, 4),
        "final_score": final_score,
        "severity": get_severity_band(final_score),
        "factors": factors_dict if factors_dict else None,
    }


def evaluate_aivss_ssvc(
    likelihood: float,
    autonomy_level: str,
    safety_criticality: str,
) -> dict[str, Any]:
    """Execute AIVSS-SSVC decision tree evaluation based on CISA/CMU stakeholder categorization."""
    level_key = autonomy_level.strip().lower()
    if level_key not in AUTONOMY_LEVELS:
        valid_levels = ", ".join(AUTONOMY_LEVELS.keys())
        raise ValueError(
            f"Invalid autonomy level '{autonomy_level}'. Must be one of: {valid_levels}"
        )

    crit_key = safety_criticality.strip().lower()
    if crit_key not in SAFETY_CRITICALITY:
        valid_crits = ", ".join(SAFETY_CRITICALITY.keys())
        raise ValueError(
            f"Invalid safety criticality '{safety_criticality}'. Must be one of: {valid_crits}"
        )

    if likelihood < 0.0 or likelihood > 1.0:
        raise ValueError(f"Likelihood must be between 0.0 and 1.0 (got {likelihood})")

    auto_info = AUTONOMY_LEVELS[level_key]
    crit_info = SAFETY_CRITICALITY[crit_key]

    risk_score = likelihood * auto_info["multiplier"] * crit_info["multiplier"]

    # Stakeholder Decision Outcome Mapping
    if risk_score >= 16.0 or (auto_info["multiplier"] >= 8.0 and risk_score >= 8.0):
        decision = "Immediate"
        sla = "0 to 7 days"
        action = "Emergency hotfix; immediate runtime isolation or execution halt"
    elif risk_score >= 8.0:
        decision = "Out-of-Cycle"
        sla = "7 to 30 days"
        action = "Expedited out-of-cycle remediation; prioritize in current development cycle"
    elif risk_score >= 3.0:
        decision = "Attend"
        sla = "30 to 60 days"
        action = "Schedule remediation in forthcoming routine maintenance sprint"
    else:
        decision = "Track"
        sla = "60 to 90+ days"
        action = "Track vulnerability telemetry; remediate during normal architectural updates"

    return {
        "framework": "AIVSS-SSVC",
        "likelihood": round(likelihood, 4),
        "autonomy_level": {
            "key": level_key,
            "name": auto_info["name"],
            "multiplier": auto_info["multiplier"],
            "description": auto_info["description"],
        },
        "safety_criticality": {
            "key": crit_key,
            "name": crit_info["name"],
            "multiplier": crit_info["multiplier"],
            "description": crit_info["description"],
        },
        "risk_score": round(risk_score, 2),
        "decision": decision,
        "remediation_sla": sla,
        "recommended_action": action,
    }


def format_text_output(
    v08_result: dict[str, Any], ssvc_result: dict[str, Any] | None = None
) -> str:
    """Format combined AIVSS scoring results for terminal output."""
    lines: list[str] = [
        "=" * 68,
        "Artificial Intelligence Vulnerability Scoring System (AIVSS v0.8)",
        "=" * 68,
        f"CVSS Baseline Score:    {v08_result['cvss_base']:.1f}"
        + (f" ({v08_result['cvss_vector']})" if v08_result.get("cvss_vector") else ""),
        f"Score Headroom (10-Base): {v08_result['headroom']:.2f}",
        f"Amplification Factor Sum: {v08_result['factor_sum']:.2f} / 10.00",
        f"Threat Multiplier (ThM):  {v08_result['threat_multiplier']:.2f}",
        f"Agentic AI Risk (AARS):   +{v08_result['aars']:.4f}",
        f"Unmitigated Score:       {v08_result['unmitigated_score']:.2f}",
        f"Mitigation Factor:        {v08_result['mitigation_factor']:.2f}",
        "-" * 68,
        f"Final AIVSS Score:        {v08_result['final_score']:.1f}",
        f"Qualitative Severity:     {v08_result['severity']}",
        "=" * 68,
    ]

    if v08_result.get("factors"):
        lines.append("Individual Amplification Factor Breakdown (F1..F10):")
        for f_code, info in sorted(v08_result["factors"].items()):
            lines.append(
                f"  {f_code:3}: {info['value']:4.1f} | {info['name']:32} ({info['description']})"
            )
        lines.append("-" * 68)

    if ssvc_result:
        lines.extend(
            [
                "AIVSS-SSVC Stakeholder Decision Matrix",
                "-" * 68,
                f"Exploitation Likelihood: {ssvc_result['likelihood']:.2f}",
                f"Agent Autonomy Level:    {ssvc_result['autonomy_level']['name']} ({ssvc_result['autonomy_level']['multiplier']:.1f}x exposure)",
                f"Safety Criticality:      {ssvc_result['safety_criticality']['name']} ({ssvc_result['safety_criticality']['multiplier']:.1f}x multiplier)",
                f"Calculated Risk Score:   {ssvc_result['risk_score']:.2f}",
                f"Decision Outcome:        {ssvc_result['decision']}",
                f"Remediation Window (SLA): {ssvc_result['remediation_sla']}",
                f"Recommended Action:      {ssvc_result['recommended_action']}",
                "=" * 68,
            ]
        )

    return "\n".join(lines)


def run_benchmark_tests() -> int:
    """Execute benchmark verification suite against published reference scenarios."""
    print("Running AIVSS Calculation Benchmark Suite...\n")

    # Benchmark 1: NVIDIA NOOA Reference Scenario (Report Benchmark)
    # CVSS Base: 8.7, Factor Sum: 7.5, ThM: 0.97, Mitigation: 1.00 -> Expected: 9.6 Critical
    res = calculate_aivss_v08(
        cvss_base=8.7,
        factor_sum=7.5,
        thm=0.97,
        mitigation=1.00,
    )
    expected_score = 9.6
    expected_sev = "Critical"
    score_ok = math.isclose(res["final_score"], expected_score, abs_tol=0.05)
    sev_ok = res["severity"].lower() == expected_sev.lower()
    status1 = "PASS" if (score_ok and sev_ok) else "FAIL"

    print(f"[{status1}] AIVSS v0.8 Benchmark (NVIDIA NOOA Reference Flaw)")
    print(
        f"       Calculated: {res['final_score']} ({res['severity']}) | Expected: {expected_score} ({expected_sev})"
    )
    print(f"       AARS: +{res['aars']} | Unmitigated: {res['unmitigated_score']}\n")

    # Benchmark 2: AIVSS-SSVC Decision Evaluation (Prime Mover with High Likelihood)
    ssvc = evaluate_aivss_ssvc(
        likelihood=0.40,
        autonomy_level="prime_mover",
        safety_criticality="critical",
    )
    expected_decision = "Immediate"
    decision_ok = ssvc["decision"].lower() == expected_decision.lower()
    status2 = "PASS" if decision_ok else "FAIL"

    print(f"[{status2}] AIVSS-SSVC Benchmark (Prime Mover / Critical Safety)")
    print(
        f"       Risk Score: {ssvc['risk_score']} | Decision: {ssvc['decision']} (SLA: {ssvc['remediation_sla']})\n"
    )

    return 0 if (status1 == "PASS" and status2 == "PASS") else 1


def main() -> int:
    """Parse command line arguments and execute AIVSS calculation."""
    parser = argparse.ArgumentParser(
        description="Calculate Artificial Intelligence Vulnerability Scoring System (AIVSS v0.8) and AIVSS-SSVC metrics."
    )
    parser.add_argument(
        "--cvss-base",
        type=float,
        help="Classical CVSS Base score (0.0 to 10.0)",
    )
    parser.add_argument(
        "--cvss-vector",
        "-v",
        help="CVSS vector string to automatically compute baseline score (e.g., CVSS:4.0/... or CVSS:3.1/...)",
    )
    parser.add_argument(
        "--factors",
        "-f",
        help="Comma-separated list of 10 amplification factor values (e.g., '5,4,5,4,2,4,4,4,3,2')",
    )
    parser.add_argument(
        "--factor-sum",
        type=float,
        help="Precomputed average amplification factor sum on scale 0.0 to 10.0 (e.g. 7.5)",
    )
    parser.add_argument(
        "--thm",
        type=float,
        default=1.0,
        help="Threat Multiplier between 0.5 and 1.5 (default: 1.0)",
    )
    parser.add_argument(
        "--mitigation",
        "-m",
        type=float,
        default=1.0,
        help="Mitigation Factor between 0.5 and 1.0 (default: 1.0)",
    )
    parser.add_argument(
        "--ssvc",
        action="store_true",
        help="Include AIVSS-SSVC decision tree evaluation",
    )
    parser.add_argument(
        "--likelihood",
        type=float,
        default=0.4,
        help="Exploitation likelihood for SSVC (0.0 to 1.0, default: 0.4)",
    )
    parser.add_argument(
        "--autonomy",
        choices=["advisor", "collaborator", "delegator", "prime_mover"],
        default="prime_mover",
        help="Agent autonomy level for SSVC (default: prime_mover)",
    )
    parser.add_argument(
        "--safety",
        choices=["low", "medium", "high", "critical"],
        default="high",
        help="Safety criticality for SSVC (default: high)",
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
        help="Run built-in benchmark validation tests",
    )

    args = parser.parse_args()

    if args.test:
        return run_benchmark_tests()

    # Determine CVSS Base score
    base_score: float | None = args.cvss_base
    vector_str: str | None = args.cvss_vector

    if vector_str and base_score is None:
        try:
            base_score, _ = resolve_cvss_base(vector_str)
        except (
            ValueError,
            CVSS2MalformedError,
            CVSS3MalformedError,
            CVSS4MalformedError,
        ) as exc:
            print(f"Error parsing CVSS vector: {exc}", file=sys.stderr)
            return 1

    if base_score is None:
        if sys.stdin.isatty():
            print(
                "No CVSS Base score or vector provided. Running built-in test suite:\n"
            )
            return run_benchmark_tests()
        parser.print_help()
        return 1

    # Parse individual factors if provided
    factors_list: list[float] | None = None
    if args.factors:
        try:
            factors_list = [float(x.strip()) for x in args.factors.split(",")]
        except ValueError:
            print(
                "Error: --factors must be a comma-separated list of numbers (e.g. '5,4,5,4,2,4,4,4,3,2')",
                file=sys.stderr,
            )
            return 1

    # Default to factor-sum 5.0 if neither factor-sum nor factors provided
    factor_sum_val = args.factor_sum
    if factors_list is None and factor_sum_val is None:
        factor_sum_val = 5.0

    try:
        v08_result = calculate_aivss_v08(
            cvss_base=base_score,
            factors=factors_list,
            factor_sum=factor_sum_val,
            thm=args.thm,
            mitigation=args.mitigation,
            cvss_vector=vector_str,
        )

        ssvc_result = None
        if args.ssvc:
            ssvc_result = evaluate_aivss_ssvc(
                likelihood=args.likelihood,
                autonomy_level=args.autonomy,
                safety_criticality=args.safety,
            )
    except (ValueError, KeyError) as err:
        if args.json:
            print(json.dumps({"error": str(err)}, indent=2))
        else:
            print(f"Calculation Error: {err}", file=sys.stderr)
        return 1

    if args.json:
        output_payload = {"aivss_v08": v08_result}
        if ssvc_result:
            output_payload["aivss_ssvc"] = ssvc_result
        print(json.dumps(output_payload, indent=2))
    else:
        print(format_text_output(v08_result, ssvc_result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
