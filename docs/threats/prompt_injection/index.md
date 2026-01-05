# <span style="color:var(--aurora)">**Prompt Injection**</span>

<br />

---
# **Description**

Prompt Injection is a threat where an attacker manipulates the inputs to alter the behavior of a GenAI system, often via user prompts, forms, or attached data. By disguising malicious inputs, an adversary can bypass guardrails and induce the AI to perform unauthorized actions, or execute arbitrary code.

!!! note
    In Gurple, distinction is made between <span style="color:var(--constellation)">**Prompt Injection**</span> and <span style="color:var(--constellation)">**Jailbreaking**</span>.
    
    The next section is dedicated to <span style="color:var(--constellation)">**Jailbreaking**</span>, which is a subset of <span style="color:var(--constellation)">**Prompt Injection**</span>. In this case, the goal is to abuse the model's safety guardrails stack (e.g., RLHF, fine-tuning, AI Judges) to generate restricted content or behaviors.

    To create a clear separation, the present section, named <span style="color:var(--constellation)">**Prompt Injection**</span>, is restricted to attacks that bypass the security layers of the GenAI system (e.g. authentication, authorization, input / output validation).

    One must also recognize that threats are not found in isolation in the wild, and that most real-world threats are chained attacks, where a hacker uses multiple techniques to achieve their goal. For example, a hacker may utilize a sequence of prompts that manipulate context to bypass the model's safety guardrails stack while also concealing inputs that will trigger code execution. In such cases, the line between <span style="color:var(--constellation)">**Prompt Injection**</span> and <span style="color:var(--constellation)">**Jailbreaking**</span> becomes blurred.


<br />

---
# **Map**

| **Framework** | **ID** | **Title** |
| :--- | :--- | :--- |
| **[Gurple](https://felipepenha.github.io/gurple/threats/)** | G-1.1 | Prompt Injection |
| **[MITRE ATLAS](https://atlas.mitre.org/matrices/ATLAS)** | [AML.TA0005](https://atlas.mitre.org/tactics/AML.TA0005) | Execution |
| **[MITRE ATLAS](https://atlas.mitre.org/matrices/ATLAS)** | [AML.T0051](https://atlas.mitre.org/techniques/AML.T0051) | LLM Prompt Injection |
| **[MITRE ATT&CK](https://attack.mitre.org/)** | [TA0002](https://attack.mitre.org/tactics/TA0002/) | Execution |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-77](https://cwe.mitre.org/data/definitions/77.html) | Improper Neutralization of Special Elements used in a Command ("Command Injection") |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-94](https://cwe.mitre.org/data/definitions/94.html) | Improper Control of Generation of Code ("Code Injection") |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-116](https://cwe.mitre.org/data/definitions/116.html) | Improper Encoding or Escaping of Output |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-1426](https://cwe.mitre.org/data/definitions/1426.html) | Improper Validation of Generative AI Output |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-1427](https://cwe.mitre.org/data/definitions/1427.html) | Improper Neutralization of Input Used for LLM Prompting |
| **[NIST AI 100-2 E2023](https://doi.org/10.6028/NIST.AI.100-2e2023)** | [3.3](https://doi.org/10.6028/NIST.AI.100-2e2023) | Direct Prompt Injection Attacks and Mitigations |
| **[NIST AI 100-2 E2025](https://doi.org/10.6028/NIST.AI.100-2e2025)** | [NISTAML.018:2025](https://doi.org/10.6028/NIST.AI.100-2e2025) | Prompt Injection |
| **[OWASP Top 10](https://owasp.org/www-project-top-ten/)** | [A03:2021](https://owasp.org/Top10/2021/A03_2021-Injection/) | Injection |
| **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** | [LLM01:2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) | Prompt Injection |
| **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** | [LLM05:2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) | Improper Output Handling[^1] |
| **[OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** | [ASI01:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Agent Goal Hijack |
| **[Pangea Taxonomy of Prompt Injection](https://pangea.cloud/taxonomy/)**| [IM0001](https://pangea.cloud/taxonomy/#IM0001) | Direct Prompt Injection (Attacker Submitted Prompt) |
| **[Pangea Taxonomy of Prompt Injection](https://pangea.cloud/taxonomy/)**| [IM0002](https://pangea.cloud/taxonomy/#IM0002) | Attacker-Submitted Prompt Body Injection |
| **[Pangea Taxonomy of Prompt Injection](https://pangea.cloud/taxonomy/)**| [IM0003](https://pangea.cloud/taxonomy/#IM0001) | Attacker-Submitted Attached Data Injection |

[^1]: Improper Output Handling is a Vulnerability that is central to the vast majority of Prompt Injection Threats, although listed separately in the OWASP Top 10 for LLM Applications. The reason is that OWASP Top 10 framework does not make a distinction between Threats and Vulnerabilities based on [SCF C|P-RMM](../../threat_vulnerability_risk/scf_cp_rmm.md), as Gurple does.