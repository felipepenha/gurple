# <span style="color:var(--aurora)">**Workflow Injection**</span>

<br />

------------------------------------------------------------------------

# **Description**

Workflow Injection differs from prompt injection by targeting the workflow engine itself rather than the LLM’s context. Attackers inject malicious configuration sequences, environment variables, code snippets, or serialized objects directly into the workflow definition (e.g., n8n JSON, LangGraph checkpoints, YAML pipelines). When processed by the workflow engine, this injected logic bypasses controls and executes arbitrary system commands (RCE), deserializes untrusted objects, or alters the intended flow of operations.

<br />

------------------------------------------------------------------------

# **Map**

| **Framework**                                                  | **ID**                                                         | **Title**                                           |
|:---------------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------|
| **[Gurple](https://felipepenha.github.io/gurple/threats/)**    | G-1.2                                                          | Workflow Injection                                  |
| **[MITRE CAPEC](https://capec.mitre.org/)**                    | [CAPEC-152](https://capec.mitre.org/data/definitions/152.html) | CAPEC CATEGORY: Inject Unexpected Items             |
| **[MITRE CAPEC](https://capec.mitre.org/)**                    |                                                                |                                                     |
| [CAPEC-176](https://capec.mitre.org/data/definitions/176.html) | Configuration/Environment Manipulation                         |                                                     |
| **[MITRE CWE](https://cwe.mitre.org/)**                        | [CWE-15](https://cwe.mitre.org/data/definitions/15.html)       | External Control of System or Configuration Setting |
| **[OWASP Top 10](https://owasp.org/www-project-top-ten/)**     | [A03:2021](https://owasp.org/Top10/2021/A03_2021-Injection/)   | Injection                                           |
