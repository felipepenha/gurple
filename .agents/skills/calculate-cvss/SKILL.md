---
name: calculate-cvss
description: Calculate Common Vulnerability Scoring System (CVSS) scores across versions 2.0, 3.0, 3.1, and 4.0 using official FIRST specifications, vector parsing, and Python automation.
---

# Calculating Common Vulnerability Scoring System Metrics

This skill governs the evaluation, vector parsing, and mathematical score calculation for the Common Vulnerability Scoring System (CVSS) across all historical and active revisions published by the Forum of Incident Response and Security Teams (FIRST).

---

## Architectural Overview of the Scoring Framework

The Common Vulnerability Scoring System provides an open, standardized method to communicate the technical characteristics and severity of software and hardware flaws. Rather than relying on subjective severity classifications, CVSS uses a composite vector of categorical values that resolve into a numerical score between 0.0 and 10.0.

The scoring framework divides metrics into functional groupings that reflect the intrinsic qualities of a vulnerability, changes over time, and environmental factors specific to a deployment. Four primary specification generations define the standard:

1. **Version 2.0 (June 2007)**: Established the tripartite division of Base, Temporal, and Environmental metric groups, alongside early impact sub-score equations.
2. **Version 3.0 (December 2015)**: Introduced the concept of Scope to measure whether a vulnerability in one software component affects resources beyond its security authority.
3. **Version 3.1 (June 2019)**: Clarified metric definitions, resolved ambiguities in Privileges Required and Scope, and standardized guidance for scoring shared software libraries without changing baseline mathematical formulas.
4. **Version 4.0 (November 2023)**: Replaced the traditional Base-Temporal-Environmental inheritance model with four distinct scoring nomenclatures (CVSS-B, CVSS-BT, CVSS-BE, and CVSS-BTE), separated Vulnerable System impacts from Subsequent System impacts, introduced Attack Requirements, and shifted calculation to non-linear MacroVectors with empirical interpolation.

---

## Common Vulnerability Scoring System Specification Versions

### Version 2.0 Historical Foundations and Metrics

CVSS version 2.0 structures baseline vulnerability analysis around six base metrics. Access Vector (AV) records whether an attacker requires local access, adjacent network access, or remote network connectivity. Access Complexity (AC) rates the technical complexity of the exploit as High, Medium, or Low. Authentication (Au) measures the count of authentication barriers an attacker must pass, ranging from Multiple to Single or None.

Impact metrics in version 2.0 measure Confidentiality (C), Integrity (I), and Availability (A) across three discrete tiers: None (N), Partial (P), and Complete (C). The standard computes an intermediate Impact score using an Impact Sub-Score equation:

$$\text{Impact} = 10.41 \times (1 - (1 - \text{ConfImpact}) \times (1 - \text{IntegImpact}) \times (1 - \text{AvailImpact}))$$

Exploitability combines Access Vector, Access Complexity, and Authentication:

$$\text{Exploitability} = 20 \times \text{AccessVector} \times \text{AccessComplexity} \times \text{Authentication}$$

The unadjusted Base score applies a conditional scaling function:

$$\text{BaseScore} = \text{RoundToOneDecimal}\left(\left(0.6 \times \text{Impact} + 0.4 \times \text{Exploitability} - 1.5\right) \times f(\text{Impact})\right)$$

where $f(\text{Impact}) = 0$ if $\text{Impact} = 0$, and $1.176$ otherwise.

While version 2.0 standardized baseline metrics, it lacked mechanisms to capture modern execution models such as cross-tenant hypervisor escapes, privilege escalation across authorization boundaries, and user interface deception.

### Version 3.0 Quantitative Metrics and the Introduction of Scope

Published in December 2015, CVSS version 3.0 updated metric terminology and added the Scope (S) metric. Scope captures whether a vulnerability in an authorization authority (the vulnerable component) impacts resources managed by a different authority (the impacted component).

Version 3.0 categorizes Base metrics into Exploitability and Impact:

The Exploitability group evaluates Attack Vector (AV: Network, Adjacent, Local, Physical), Attack Complexity (AC: Low, High), Privileges Required (PR: None, Low, High), and User Interaction (UI: None, Required). The score allocated to Privileges Required depends dynamically on whether Scope is Unchanged (U) or Changed (C).

The Impact group evaluates Confidentiality (C), Integrity (I), and Availability (A) across None (N), Low (L), and High (H).

The quantitative calculation in version 3.0 executes via distinct branches depending on Scope:

An intermediate Impact Sub-Score (ISS) is derived first:

$$\text{ISS} = 1 - (1 - \text{ISS}_{\text{Conf}}) \times (1 - \text{ISS}_{\text{Integ}}) \times (1 - \text{ISS}_{\text{Avail}})$$

When Scope is Unchanged:

$$\text{Impact} = 6.42 \times \text{ISS}$$

When Scope is Changed:

$$\text{Impact} = 7.52 \times (\text{ISS} - 0.029) - 3.25 \times (\text{ISS} - 0.02)^{15}$$

Exploitability sub-score aggregates the four attacker-facing values:

$$\text{Exploitability} = 8.22 \times \text{AV} \times \text{AC} \times \text{PR} \times \text{UI}$$

If $\text{Impact} \le 0$, the Base score is 0. Otherwise, the Base score combines Exploitability and Impact, rounded up using the formal `RoundUp` ceiling function:

$$\text{BaseScore}_{\text{Unchanged}} = \text{RoundUp}(\min(\text{Impact} + \text{Exploitability}, 10.0))$$

$$\text{BaseScore}_{\text{Changed}} = \text{RoundUp}(\min(1.08 \times (\text{Impact} + \text{Exploitability}), 10.0))$$

The version 3.0 `RoundUp` function rounds to the nearest single decimal place, ensuring that values with any remainder round to the next tenth (e.g., 4.02 becomes 4.1).

### Version 3.1 Clarifications and Formula Invariance

Released in June 2019, CVSS version 3.1 introduced no mathematical formula changes. All vector strings, numerical scores, and qualitative severity ratings remain identical between versions 3.0 and 3.1 for identical metric values.

Version 3.1 resolved recurring industry scoring disputes:

First, it refined the boundary between Attack Complexity (AC) and Privileges Required (PR). AC exclusively measures conditions outside the attacker's control, such as timing windows, race conditions, or specific system states. If an attacker must acquire credentials or administrative rights, that difficulty belongs under Privileges Required, not Attack Complexity.

Second, version 3.1 clarified Scope transitions. It affirmed that Scope changes occur when the impacted component belongs to a distinct security authority, such as an application escaping into the host operating system, a database plugin modifying host files, or a cross-site scripting attack executing in a victim's browser session.

Third, version 3.1 added detailed guidance for scoring software libraries, stating that library vulnerabilities must be scored in the context of a reasonable default or intended implementation rather than theoretical worst-case integrations.

### Version 4.0 The MacroVector Paradigm and Subsequent Systems

CVSS version 4.0, published in November 2023, represents a major architectural redesign of the standard. The revision addresses criticisms of score inflation, ambiguous metric combinations, and inadequate differentiation between target components and downstream systems.

#### Four Nomenclature Classes

Version 4.0 ends the practice of referring generically to a single "CVSS score." Instead, assessments must cite the specific nomenclature corresponding to the metric sets evaluated:

1. **CVSS-B**: Base metrics only.
2. **CVSS-BT**: Base and Threat metrics.
3. **CVSS-BE**: Base and Environmental metrics.
4. **CVSS-BTE**: Base, Threat, and Environmental metrics.

#### Separation of Vulnerable and Subsequent Systems

Version 4.0 replaces the single Scope metric with split impact assessments. Analysts evaluate two distinct targets:

The **Vulnerable System** refers to the software, hardware, or service hosting the flaw:
- Vulnerable System Confidentiality (VC: High, Low, None)
- Vulnerable System Integrity (VI: High, Low, None)
- Vulnerable System Availability (VA: High, Low, None)

The **Subsequent System** refers to any system or resource that suffers consequential impact through the compromised vulnerable system:
- Subsequent System Confidentiality (SC: High, Low, None)
- Subsequent System Integrity (SI: High, Low, None)
- Subsequent System Availability (SA: High, Low, None)

#### Introduction of Attack Requirements

Version 4.0 separates prerequisites from technical complexity by introducing Attack Requirements (AT):
- **Attack Requirements (AT)**: Captures prerequisite execution conditions independent of attacker actions, such as deployment architecture or specific network configurations (None [N] or Present [P]).
- **Attack Complexity (AC)**: Retains its focus on active evasion techniques or security defenses that an attacker must circumvent during execution (Low [L] or High [H]).

#### MacroVectors and Equivalence Classes

CVSS version 4.0 abandons single continuous algebraic equations. Instead, it assigns metric combinations into six Equivalence Classes (EQ1 through EQ6), forming a 6-digit MacroVector:

- **EQ1 (MacroVector Position 1)**: Exploitability metrics (AV, PR, UI). Values range from 0 to 2.
- **EQ2 (MacroVector Position 2)**: Attack Complexity and Requirements (AC, AT). Values range from 0 to 1.
- **EQ3 (MacroVector Position 3)**: Vulnerable System Impact (VC, VI, VA). Values range from 0 to 2.
- **EQ4 (MacroVector Position 4)**: Subsequent System Impact (SC, SI, SA). Values range from 0 to 2.
- **EQ5 (MacroVector Position 5)**: Threat Exploit Maturity (E). Values range from 0 to 2.
- **EQ6 (MacroVector Position 6)**: Environmental Security Requirements (CR, IR, AR) combined with Modified Subsequent impacts. Values range from 0 to 1.

The resulting MacroVector (such as `001200`) maps directly to a pre-computed lookup table defining maximum possible scores. A standardized interpolation algorithm then calculates deviations between the assigned vector and reference anchor vectors, deriving the final score with empirical precision.

---

## Qualitative Severity Ratings

Across versions 3.0, 3.1, and 4.0, numerical scores map to qualitative severity bands:

| Numerical Score Range | Qualitative Severity Rating |
| :--- | :--- |
| **0.0** | None |
| **0.1 – 3.9** | Low |
| **4.0 – 6.9** | Medium |
| **7.0 – 8.9** | High |
| **9.0 – 10.0** | Critical |

In version 2.0, only three qualitative bands existed: Low (0.0–3.9), Medium (4.0–6.9), and High (7.0–10.0).

---

## Executing the Calculation Toolchain With Astral uv

The skill companion script `scripts/calculate_cvss.py` supports automated parsing, validation, and scoring for all four CVSS revisions. The tool runs inside an isolated virtual environment managed by Astral `uv`.

### Command-Line Execution and Vector Evaluation

To calculate scores from a vector string, invoke the script using `uv run`:

```bash
# Calculate CVSS v4.0 Base Score
uv run python scripts/calculate_cvss.py -v "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"

# Calculate CVSS v3.1 Base Score
uv run python scripts/calculate_cvss.py -v "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"

# Calculate legacy CVSS v2.0 Base Score
uv run python scripts/calculate_cvss.py -v "AV:N/AC:L/Au:N/C:P/I:P/A:P"
```

The script prints the verified vector string, the calculated Base score, qualitative severity, intermediate sub-scores, MacroVectors for version 4.0, and an expanded table of metric assignments.

### Machine-Readable JSON Pipeline Integration

Pass the `--json` or `-j` flag to generate structured JSON for downstream report generation, ticketing, or agent pipelines:

```bash
uv run python scripts/calculate_cvss.py -v "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N" --json
```

Example JSON output structure:

```json
{
  "version": "4.0",
  "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N",
  "base_score": 8.7,
  "base_severity": "High",
  "macro_vector": "001200",
  "metrics": {
    "AV": { "value": "N", "description": "Network" },
    "AC": { "value": "L", "description": "Low" },
    "AT": { "value": "N", "description": "None" },
    "PR": { "value": "N", "description": "None" },
    "UI": { "value": "N", "description": "None" },
    "VC": { "value": "N", "description": "None" },
    "VI": { "value": "N", "description": "None" },
    "VA": { "value": "H", "description": "High" },
    "SC": { "value": "N", "description": "None" },
    "SI": { "value": "N", "description": "None" },
    "SA": { "value": "N", "description": "None" }
  }
}
```

### Makefile Automation Targets

The companion Makefile provides standard lifecycle commands:

- `make help`: Display available targets and runtime environment information.
- `make test`: Execute the benchmark validation suite across all four CVSS specifications.
- `make format`: Format and lint the codebase using `ruff` with zero tolerance for errors.
- `make sync`: Synchronize virtual environment packages deterministically using `uv sync`.
- `make lock`: Update dependencies in `uv.lock`.
