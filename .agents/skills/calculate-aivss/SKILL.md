---
name: calculate-aivss
description: Calculate Artificial Intelligence Vulnerability Scoring System (AIVSS) scores across the OWASP AIVSS v0.8 mathematical amplification specification and the AIVSS-SSVC decision tree framework using Python automation.
---

# Calculating Artificial Intelligence Vulnerability Scoring System Metrics

This skill governs the evaluation, metric assignment, and mathematical score calculation for the Artificial Intelligence Vulnerability Scoring System (AIVSS). It implements both the quantitative formula defined in the OWASP AIVSS version 0.8 specification and the stakeholder decision tree framework defined in AIVSS-SSVC.

---

## Architectural Foundations of Artificial Intelligence Vulnerability Scoring

Classical vulnerability scoring standards, such as CVSS, were engineered to evaluate deterministic software flaws where an exploit produces a predictable deviation in confidentiality, integrity, or availability. Autonomous agents and large language model execution loops violate these core assumptions in three foundational ways:

First, agentic software operates through non-deterministic reasoning loops. A vulnerability in an agent does not merely compromise static data; it redirects the agent's goal formation, plans, tool invocations, and subagent delegations.

Second, agentic architectures introduce unbounded blast radiuses. When an agent possesses tools allowing shell execution, file system modification, web browsing, or financial transactions, a low-severity parsing flaw in a prompt or tool parser can cascade into arbitrary remote code execution, persistent memory poisoning, or unconstrained resource exhaustion.

Third, classical CVSS does not account for agent autonomy. An identical flaw in a sandboxed summarization script behaves differently when present in an unmonitored autonomous agent operating with root execution privileges. AIVSS bridges this gap by grounding assessments in verified CVSS base scores while systematically applying risk amplification factors, autonomy multipliers, and mitigation coefficients.

---

## Evolution of Scoring Frameworks Across Specification Releases

### Early Draft Formulations and the Shift Away From Static Assumptions

Early drafts of AI security scoring (versions 0.1 through 0.5) attempted to redefine all metrics from scratch, creating proprietary access vectors and impact categories. These early revisions encountered widespread resistance because enterprise risk governance and compliance frameworks rely on established National Vulnerability Database (NVD) and CVE workflows.

Security teams required a mechanism that retained compatibility with classical vulnerability databases while reflecting the compounding exposure of generative AI execution engines. This requirement produced the dual-methodology architecture adopted in active production: the quantitative mathematical amplification model of AIVSS version 0.8 and the qualitative triage model of AIVSS-SSVC.

### The OWASP AIVSS Version 0.8 Mathematical Amplification Model

The OWASP GenAI and Agentic AI Core Security Risks Project formalized the version 0.8 specification to augment existing CVSS Base scores. Rather than replacing CVSS, AIVSS version 0.8 treats the CVSS Base score (calculated under either CVSS version 3.1 or version 4.0) as an empirical lower bound.

The mathematical model evaluates ten discrete Agentic AI Risk Amplification Factors ($F_1$ through $F_{10}$), each mapped directly to the OWASP Agentic AI Core Security Risks. These factors measure the extent to which the vulnerable architecture permits goal hijacking, memory poisoning, unvalidated tool invocation, or multi-agent cascades.

The amplification calculation derives an Agentic AI Risk Score (AARS) by scaling the remaining score headroom ($10.0 - \text{CVSS\_Base}$) against the normalized factor sum and an adversary Threat Multiplier ($\text{ThM}$). Finally, a Mitigation Factor ($M$) evaluates runtime guardrails, defense-in-depth controls, and human-in-the-loop isolation to produce a final, defensible score capped at 10.0.

### The AIVSS-SSVC Stakeholder Decision Tree Framework

Hosted at `aivss.owasp.org/ssvc.html`, the AIVSS-SSVC framework adapts the Stakeholder-Specific Vulnerability Categorization (SSVC) methodology developed by the Software Engineering Institute (SEI) at Carnegie Mellon University and the Cybersecurity and Infrastructure Security Agency (CISA).

While AIVSS version 0.8 calculates a quantitative severity number, AIVSS-SSVC establishes an operational remediation decision. It structures prioritization around three technical axes:

1. **Exploitation Likelihood**: Combines threat actor accessibility, exploit weaponization, and technical vulnerability into an empirical probability ($P(\text{Threat}) \times P(\text{Vuln})$).
2. **Agent Autonomy Level**: Evaluates the independence of the target agent loop across four discrete tiers, assigning exposure multipliers from $1.0\times$ for human-supervised advisors to $8.0\times$ for autonomous prime movers.
3. **Safety Criticality**: Evaluates the potential physical, financial, operational, or legal blast radius of the system hosting the agent.

The resulting decision output dictates unambiguous organizational action (Track, Attend, Out-of-Cycle, or Immediate) paired with enforceable remediation service level agreement (SLA) windows.

---

## Quantitative Equations and Amplification Logics

### Baseline CVSS Integration and Headroom Determination

The AIVSS version 0.8 formula establishes its baseline using a verified CVSS Base score:

$$\text{CVSS\_Base} \in [0.0, 10.0]$$

Assessments may draw this baseline from CVSS version 3.1 (`CVSS:3.1/AV:N/AC:L/...`) or CVSS version 4.0 (`CVSS:4.0/AV:N/AC:L/...`). The remaining score headroom represents the maximum possible severity increase that agentic dynamics can contribute:

$$\text{Headroom} = 10.0 - \text{CVSS\_Base}$$

If the baseline CVSS Base score is 8.7, the available headroom is $10.0 - 8.7 = 1.30$. If the baseline is 7.5, the available headroom is $2.50$.

### The Ten Agentic AI Risk Amplification Factors

Assessors evaluate the vulnerability against the ten OWASP Agentic AI Core Security Risks. Each factor receives a score from 0.0 (no exposure) to 10.0 (unconstrained exposure):

1. **Factor F1 (Goal Hijacking)**: Evaluates whether an adversary can alter the primary mission, persona, or high-level goals of the agent.
2. **Factor F2 (Prompt Injection and Jailbreak)**: Measures resistance to direct system prompt extraction, jailbreaks, or indirect prompt injection via retrieved content.
3. **Factor F3 (Sensitive Information Disclosure)**: Assesses the risk of private system data, API keys, credentials, or context leakage.
4. **Factor F4 (Supply Chain)**: Evaluates third-party model weights, unsafe serialization formats, untrusted Python packages, or insecure MCP server extensions.
5. **Factor F5 (Execution Engine Hijacking)**: Measures exposure of code execution runtimes, shell environments, sandboxes, or container namespaces.
6. **Factor F6 (Insecure Function Calling)**: Evaluates whether tools, APIs, and client methods validate arguments or enforce parameter boundaries.
7. **Factor F7 (Excessive Agency and Privilege Creep)**: Assesses whether the agent possesses unnecessary administrative privileges, unattended loops, or missing human approval gates.
8. **Factor F8 (Memory and State Poisoning)**: Measures vulnerability of long-term semantic memories, conversation scratchpads, session databases, or vector indexes to persistent poisoning.
9. **Factor F9 (Multi-Agent Cascade)**: Evaluates whether corrupted agent decisions propagate downstream to compromise peer or child agents.
10. **Factor F10 (Denial of Wallet and Resource Exhaustion)**: Assesses vulnerability to infinite recursive agent loops, token flooding, API billing exhaustion, or CPU/GPU starvation.

The factors aggregate into a normalized Factor Sum on a 0.0 to 10.0 scale:

$$\text{Factor\_Sum} = \frac{\sum_{i=1}^{10} F_i}{10.0}$$

Alternatively, assessors may establish category sub-averages across Architectural, Operational, and Environmental groupings to determine the aggregate Factor Sum directly.

### Threat Multipliers and Mitigation Coefficients

The intermediate Agentic AI Risk Score (AARS) scales the headroom through the normalized factor ratio and the Threat Multiplier:

$$\text{AARS} = (10.0 - \text{CVSS\_Base}) \times \left(\frac{\text{Factor\_Sum}}{10.0}\right) \times \text{ThM}$$

The **Threat Multiplier ($\text{ThM}$)** reflects adversary reach, capability, and exploit weaponization:
- **0.50 – 0.80**: Low capability; theoretical exploit requiring physical access or obscure configurations.
- **0.90 – 1.10**: Standard capability; remote network adversary using public tools or straightforward payloads.
- **1.20 – 1.50**: Advanced persistent adversary; weaponized automated exploit chains or coordinated campaigns.

The **Mitigation Factor ($M$)** evaluates existing operational defenses and architectural guardrails:
- **1.00**: No mitigations present, or existing controls bypassed completely.
- **0.80 – 0.95**: Partial mitigations; heuristic prompt filters, basic output token limits, or post-execution logging without blocking.
- **0.50 – 0.75**: Comprehensive mitigations; isolated microVM sandboxing, cryptographic tool call verification, read-only state boundaries, and strict human authorization gates.

The final AIVSS version 0.8 score calculates as:

$$\text{AIVSS} = \min\left(10.0, \text{RoundHalfUp}\left((\text{CVSS\_Base} + \text{AARS}) \times M, 1\right)\right)$$

Numerical scores map to qualitative severity ratings:
- **0.0**: None
- **0.1 – 3.9**: Low
- **4.0 – 6.9**: Medium
- **7.0 – 8.9**: High
- **9.0 – 10.0**: Critical

---

## Stakeholder Categorization and Autonomy Multipliers

### The Four Tiers of Agent Autonomy

AIVSS-SSVC structures agent exposure around the degree of human involvement in the decision and action cycle:

1. **Advisor ($1.0\times$ Multiplier)**: The agent functions in an advisory capacity. It generates suggestions, drafts, or analysis, but all state-changing actions require direct human execution.
2. **Collaborator ($2.0\times$ Multiplier)**: The agent executes tasks in a co-piloted configuration. It prepares actions automatically, but critical tool calls or destructive operations require explicit human confirmation.
3. **Delegator ($4.0\times$ Multiplier)**: The agent operates autonomously within bounded administrative scopes. It invokes tools and executes tasks without interactive human prompts, notifying humans asynchronously upon completion or error.
4. **Prime Mover ($8.0\times$ Multiplier)**: The agent operates with complete end-to-end autonomy. It possesses self-directed task formulation, recursive subagent spawning, dynamic tool selection, and unmonitored runtime privileges. Compromise at this level grants the adversary full operational proxy capability.

### Safety Criticality and Blast Radius

Safety criticality measures the intrinsic consequences of failure:
- **Low ($1.0\times$ Multiplier)**: Read-only summarization, internal developer testing, or isolated non-production experiments.
- **Medium ($2.0\times$ Multiplier)**: Departmental business automation, non-confidential customer support, or localized data transformations.
- **High ($3.0\times$ Multiplier)**: Enterprise business operations, confidential customer data pipelines, financial transaction processing, or continuous deployment pipelines.
- **Critical ($4.0\times$ Multiplier)**: Safety-of-life systems, healthcare diagnostic and treatment pipelines, critical national infrastructure, or root corporate authorization control.

### Decision Outcomes and Remediation Windows

The composite Risk Score derives from the product of likelihood, autonomy, and criticality:

$$\text{Risk Score} = \text{Likelihood} \times \text{Autonomy Multiplier} \times \text{Safety Criticality Multiplier}$$

This score resolves into four discrete operational decisions:

| Calculated Risk Score | SSVC Decision | Remediation SLA Window | Operational Action |
| :--- | :--- | :--- | :--- |
| **$\ge 16.0$** (or Prime Mover with score $\ge 8.0$) | **Immediate** | **0 to 7 Days** | Emergency out-of-band hotfix; immediately disable agent tool execution or isolate runtime. |
| **8.0 – 15.9** | **Out-of-Cycle** | **7 to 30 Days** | Prioritize remediation outside the normal sprint cycle; deploy temporary guardrails. |
| **3.0 – 7.9** | **Attend** | **30 to 60 Days** | Remediate during the next scheduled maintenance or regular engineering cycle. |
| **$< 3.0$** | **Track** | **60 to 90+ Days** | Monitor vulnerability telemetry; remediate during routine system refactoring. |

---

## Executing the Calculation Toolchain With Astral uv

The skill companion script `scripts/calculate_aivss.py` implements both the quantitative AIVSS version 0.8 formula and the qualitative AIVSS-SSVC decision tree matrix. It runs through an isolated virtual environment managed by Astral `uv`.

### Command-Line Execution and Vector Evaluation

To calculate scores using an existing CVSS vector string, supply the vector alongside factor ratings and multipliers:

```bash
# Calculate AIVSS v0.8 using a CVSS v4.0 vector baseline and precomputed factor sum
uv run python scripts/calculate_aivss.py \
  -v "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N" \
  --factor-sum 7.5 \
  --thm 0.97 \
  --mitigation 1.0

# Calculate AIVSS v0.8 with individual factor scores and SSVC decision evaluation
uv run python scripts/calculate_aivss.py \
  --cvss-base 8.7 \
  --factors "5,4,5,4,2,4,4,4,3,2" \
  --thm 0.97 \
  --mitigation 1.0 \
  --ssvc \
  --likelihood 0.40 \
  --autonomy prime_mover \
  --safety critical
```

The tool prints the baseline score, headroom, amplification factor sum, threat multiplier, unmitigated score, final score, qualitative severity rating, and the SSVC decision matrix.

### Machine-Readable JSON Pipeline Integration

Pass the `--json` or `-j` flag to generate structured JSON payloads for vulnerability disclosure reports, issue trackers, and automated triage pipelines:

```bash
uv run python scripts/calculate_aivss.py \
  --cvss-base 8.7 \
  --factor-sum 7.5 \
  --thm 0.97 \
  --mitigation 1.0 \
  --ssvc \
  --likelihood 0.40 \
  --autonomy prime_mover \
  --safety critical \
  --json
```

Example JSON output structure:

```json
{
  "aivss_v08": {
    "framework": "AIVSS v0.8",
    "cvss_base": 8.7,
    "cvss_vector": null,
    "headroom": 1.3,
    "factor_sum": 7.5,
    "threat_multiplier": 0.97,
    "aars": 0.94575,
    "unmitigated_score": 9.6457,
    "mitigation_factor": 1.0,
    "final_score": 9.6,
    "severity": "Critical",
    "factors": null
  },
  "aivss_ssvc": {
    "framework": "AIVSS-SSVC",
    "likelihood": 0.4,
    "autonomy_level": {
      "key": "prime_mover",
      "name": "Prime Mover",
      "multiplier": 8.0,
      "description": "Fully autonomous execution, unmonitored agent loops, or root execution rights"
    },
    "safety_criticality": {
      "key": "critical",
      "name": "Critical",
      "multiplier": 4.0,
      "description": "Safety-of-life, irreversible system compromise, or unbounded liability"
    },
    "risk_score": 12.8,
    "decision": "Immediate",
    "remediation_sla": "0 to 7 days",
    "recommended_action": "Emergency hotfix; immediate runtime isolation or execution halt"
  }
}
```

### Makefile Automation Targets

The companion Makefile provides standard lifecycle commands:

- `make help`: Display available targets and runtime environment information.
- `make test`: Execute the benchmark validation suite against reference scenarios.
- `make format`: Format and lint the codebase using `ruff` with zero tolerance for errors.
- `make sync`: Synchronize virtual environment packages deterministically using `uv sync`.
- `make lock`: Update dependencies in `uv.lock`.
