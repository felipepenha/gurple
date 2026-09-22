# <span style="color:var(--aurora)">**Jailbreaking**</span>

<br />

---
# **Description**

Jailbreaking is a threat where an adversary crafts adversarial prompts to bypass the safety alignment, content moderation filters, and behavioral guardrails of a Large Language Model (LLM). Rather than targeting application permissions or host execution layers, jailbreaking exploits the model's instruction-following nature to elicit prohibited, hazardous, or policy-violating outputs that the system was trained to refuse.

Adversaries achieve jailbreaks by exploiting the fundamental tension between helpfulness and safety in aligned models. Through techniques such as persona adoption, adversarial suffix optimization, linguistic ciphering, multi-turn escalation, and hypothetical context framing, the input forces the model's objective of fulfilling user requests to override its refusal mechanisms.

!!! note
    Refer to the note in the [Prompt Injection](../prompt_injection/index.md#description) section for the distinction between <span style="color:var(--constellation)">**Prompt Injection**</span> and <span style="color:var(--constellation)">**Jailbreaking**</span>.


<br />

---
# **Map**

| **Framework** | **ID** | **Title** |
| :--- | :--- | :--- |
| **[Gurple](https://felipepenha.github.io/gurple/threats/)** | G-0.2 | Jailbreaking |
| **[MITRE ATLAS](https://atlas.mitre.org/matrices/ATLAS)** | [AML.TA0007](https://atlas.mitre.org/tactics/AML.TA0007) | Defense Evasion |
| **[MITRE ATLAS](https://atlas.mitre.org/matrices/ATLAS)** | [AML.T0054](https://atlas.mitre.org/techniques/AML.T0054) | LLM Jailbreak |
| **[MITRE ATT&CK](https://attack.mitre.org/)** | [TA0005](https://attack.mitre.org/tactics/TA0005/) | Defense Evasion |
| **[MITRE ATT&CK](https://attack.mitre.org/)** | [T1562](https://attack.mitre.org/techniques/T1562/) | Impair Defenses |
| **[MITRE CAPEC](https://capec.mitre.org/)** | [CAPEC-554](https://capec.mitre.org/data/definitions/554.html) | Functionality Bypass |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-184](https://cwe.mitre.org/data/definitions/184.html) | Incomplete List of Disallowed Inputs |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-693](https://cwe.mitre.org/data/definitions/693.html) | Protection Mechanism Failure |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-1427](https://cwe.mitre.org/data/definitions/1427.html) | Improper Neutralization of Input Used for LLM Prompting |
| **[NIST AI 100-2 E2023](https://doi.org/10.6028/NIST.AI.100-2e2023)** | [3.3](https://doi.org/10.6028/NIST.AI.100-2e2023) | Direct Prompt Injection Attacks and Mitigations |
| **[NIST AI 100-2 E2025](https://doi.org/10.6028/NIST.AI.100-2e2025)** | [NISTAML.018:2025](https://doi.org/10.6028/NIST.AI.100-2e2025) | Prompt Injection |
| **[OWASP Top 10](https://owasp.org/www-project-top-ten/)** | [A03:2021](https://owasp.org/Top10/2021/A03_2021-Injection/) | Injection |
| **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** | [LLM01:2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) | Prompt Injection |
| **[OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** | [ASI01:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Agent Goal Hijack |