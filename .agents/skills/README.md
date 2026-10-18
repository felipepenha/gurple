# Gurple Agent Skills

This directory maintains runnable agent skills for [Gurple — GenAI Security for Purple Teams](https://felipepenha.github.io/gurple/).

---

## Overview

Agent skills package reusable domain knowledge, automation scripts, reference standards, and decision trees for AI coding assistants and autonomous agents. Each skill defines its behavioral triggers and operational instructions within a `SKILL.md` specification file.

While Gurple relies on internal authoring skills for documentation generation, the repository exposes dedicated public scoring skills under `.agents/skills/` to assist security engineers, red teams, and blue teams during vulnerability assessments.

---

## Installing Skills With the npx CLI

Agent skills can be installed directly into any workspace or AI agent environment using the open-source `skills` CLI ([skills.sh](https://skills.sh)). The tool downloads skill definitions directly from Git repositories into local agent directories without requiring manual file copying.

### Installing From the Gurple Repository

To install all public skills from Gurple into the active project directory:

```bash
npx skills add felipepenha/gurple
```

To install an individual skill directly by URL:

```bash
# Install the FIRST CVSS scoring skill
npx skills add https://github.com/felipepenha/gurple/tree/main/.agents/skills/calculate-cvss

# Install the OWASP AIVSS scoring skill
npx skills add https://github.com/felipepenha/gurple/tree/main/.agents/skills/calculate-aivss
```

### Global Installation

To make a skill accessible across all local projects rather than scoping it to a single workspace, supply the global flag:

```bash
npx skills add https://github.com/felipepenha/gurple/tree/main/.agents/skills/calculate-cvss -g
```

### Skill Lifecycle Management

The `skills` CLI provides standard subcommands to audit, inspect, update, and remove installed skills:

```bash
# List all active skills installed in the current environment
npx skills list

# Check installed skills against their remote Git origins
npx skills check

# Update installed skills to the latest commit on main
npx skills update

# Remove a previously installed skill
npx skills remove calculate-cvss
```

---

## Available Public Skills

The Gurple repository publishes two automated scoring skills for public integration.

### Common Vulnerability Scoring System (calculate-cvss)

Located in [`.agents/skills/calculate-cvss/`](calculate-cvss/), this skill calculates severity metrics across all four official specification versions published by the Forum of Incident Response and Security Teams (FIRST): CVSS 2.0, 3.0, 3.1, and 4.0.

The skill inspects raw CVSS vector strings, validates metric keys and allowable levels, and evaluates Base, Threat/Temporal, and Environmental metric groups. For CVSS version 4.0, the implementation computes the non-linear MacroVector combinations and applies equivalent class interpolation to produce CVSS-B, CVSS-BT, CVSS-BE, and CVSS-BTE ratings.

Security engineers and purple teams use this skill during triage to establish baseline severity for conventional software flaws embedded within model runtimes, orchestration engines, and tool execution boundaries.

Command line invocation example:

```bash
uv run python .agents/skills/calculate-cvss/scripts/calculate_cvss.py --vector "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"
```

### Artificial Intelligence Vulnerability Scoring System (calculate-aivss)

Located in [`.agents/skills/calculate-aivss/`](calculate-aivss/), this skill provides automated scoring for probabilistic vulnerabilities in Large Language Models and autonomous agent systems where classical deterministic assumptions fail.

The skill implements both production evaluation methodologies established by the project:

1. **OWASP AIVSS Mathematical Amplification (v0.8)**: Takes verified CVSS Base vectors and applies multiplicative weighting factors for autonomy level, prompt blast radius, vector memory poisoning, tool execution authority, and active runtime guardrail coefficients.
2. **AIVSS-SSVC Qualitative Decision Trees**: Implements the Stakeholder-Specific Vulnerability Categorization decision tree tailored for AI systems, evaluating exploitation state, system utility, technical impact, safety impact, and mission impact to produce actionable triage outcomes (Track, Track*, Attend, Act).

Command line invocation example:

```bash
uv run python .agents/skills/calculate-aivss/scripts/calculate_aivss.py --spec amplification --base 7.5 --autonomy high --blast-radius broad --guardrails partial
```
