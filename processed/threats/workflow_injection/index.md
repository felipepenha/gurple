# <span style="color:var(--aurora)">**Workflow Injection**</span>

<br />

------------------------------------------------------------------------

# **Description**

Workflow Injection differs from prompt injection by targeting the workflow engine itself rather than the LLM’s context. Attackers inject malicious configuration sequences, environment variables, code snippets, or serialized objects directly into the workflow definition (e.g., n8n JSON, LangGraph checkpoints, YAML pipelines). When processed by the workflow engine, this injected logic bypasses controls and executes arbitrary system commands (RCE), deserializes untrusted objects, or alters the intended flow of operations.

<br />

------------------------------------------------------------------------

# **Map**

| **Framework**                                                                                                                 | **ID**                                                                                               | **Title**                                                                                        |
|:------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------|
| **[Gurple](https://felipepenha.github.io/gurple/threats/)**                                                                   | G-0.3                                                                                                | Workflow Injection                                                                               |
| **[SCF C\|P-RMM](https://securecontrolsframework.com/free/risk-management-model/)**                                           | [R-BC-4](https://securecontrolsframework.com/free/risk-management-model/)                            | Business Continuity & Information loss / corruption or system compromise due to technical attack |
| **[CSA MAESTRO](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro)**             | [L3](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro) | Agent Orchestration Layer (Task Execution & Workflow State Hijack)                               |
| **[MITRE ATLAS](https://atlas.mitre.org/matrices/ATLAS)**                                                                     | [AML.TA0005](https://atlas.mitre.org/tactics/AML.TA0005)                                             | Execution                                                                                        |
| **[MITRE ATT&CK](https://attack.mitre.org/)**                                                                                 | [TA0002](https://attack.mitre.org/tactics/TA0002/)                                                   | Execution                                                                                        |
| **[MITRE CAPEC](https://capec.mitre.org/)**                                                                                   | [CAPEC-152](https://capec.mitre.org/data/definitions/152.html)                                       | Inject Unexpected Items                                                                          |
| **[MITRE CAPEC](https://capec.mitre.org/)**                                                                                   | [CAPEC-176](https://capec.mitre.org/data/definitions/176.html)                                       | Configuration/Environment Manipulation                                                           |
| **[MITRE CWE](https://cwe.mitre.org/)**                                                                                       | [CWE-15](https://cwe.mitre.org/data/definitions/15.html)                                             | External Control of System or Configuration Setting                                              |
| **[MITRE CWE](https://cwe.mitre.org/)**                                                                                       | [CWE-94](https://cwe.mitre.org/data/definitions/94.html)                                             | Improper Control of Generation of Code (“Code Injection”)                                        |
| **[NIST AI 100-2 E2023](https://doi.org/10.6028/NIST.AI.100-2e2023)**                                                         | [3.3.2](https://doi.org/10.6028/NIST.AI.100-2e2023)                                                  | Indirect Prompt Injection                                                                        |
| **[NIST AI 100-2 E2025](https://doi.org/10.6028/NIST.AI.100-2e2025)**                                                         | [NISTAML.015:2025](https://doi.org/10.6028/NIST.AI.100-2e2025)                                       | Indirect Prompt Injection                                                                        |
| **[OWASP Top 10](https://owasp.org/www-project-top-ten/)**                                                                    | [A03:2021](https://owasp.org/Top10/2021/A03_2021-Injection/)                                         | Injection                                                                                        |
| **[OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** | [ASI01:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)       | Agent Goal Hijack                                                                                |
| **[OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** | [ASI02:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)       | Tool Misdirection                                                                                |
| **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)**          | [LLM08:2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)               | Agency and Autonomous Action                                                                     |
