# <span style="color:var(--aurora)">**Model Tampering**</span>

<br />

------------------------------------------------------------------------

# **Description**

Model Tampering encompasses unauthorized modifications to model parameters, training sets, fine-tuning corpora, activation spaces, or artifact serialization formats. Adversaries manipulate the machine learning lifecycle to implant covert behaviors, bypass safety alignments, or degrade inference integrity. Rather than exploiting ephemeral conversational prompts at runtime, model tampering alters the static artifacts and parameter matrices that govern model behavior.

Adversaries achieve model tampering across distinct development phases. During data collection and fine-tuning, attackers inject corrupted records or biased preference pairs. In post-training and supply chain distribution, attackers execute direct numerical updates against weight tensors, distribute trojaned parameter-efficient fine-tuning (PEFT) adapters, or blend unaligned models through weight merging. The resulting models maintain nominal benchmark performance on standard inputs, but produce malicious outputs or grant administrative execution capabilities when triggered.

- !!! note
  In Gurple, a structural distinction exists between <span style="color:var(--constellation)">**Model Tampering**</span>, <span style="color:var(--constellation)">**Prompt Injection**</span>, and <span style="color:var(--constellation)">**Poisoning**</span>.

  <span style="color:var(--constellation)">**Prompt Injection**</span> manipulates the transient conversational context within the model’s inference window, leaving the underlying neural network parameters unchanged.

  <span style="color:var(--constellation)">**Poisoning**</span> targets external runtime data stores, such as semantic cache memory, agent session logs, or retrieval-augmented generation (RAG) vector stores.

  <span style="color:var(--constellation)">**Model Tampering**</span> targets the computational foundation itself, modifying training datasets, fine-tuning corpora, model weights, or serialized model files.

<br />

------------------------------------------------------------------------

# **Map**

| **Framework** | **ID** | **Title** |
|:---|:---|:---|
| **[Gurple](https://felipepenha.github.io/gurple/threats/)** | G-0.4 | Model Tampering |
| **[SCF C\|P-RMM](https://securecontrolsframework.com/free/risk-management-model/)** | [R-BC-4](https://securecontrolsframework.com/free/risk-management-model/) | Business Continuity & Information loss / corruption or system compromise due to technical attack |
| **[CSA LLM Threats Taxonomy](https://cloudsecurityalliance.org/artifacts/csa-large-language-model-llm-threats-taxonomy)** | [Model Manipulation](https://cloudsecurityalliance.org/artifacts/csa-large-language-model-llm-threats-taxonomy) | Model Manipulation |
| **[CSA MAESTRO](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro)** | [L1](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro) | Agent Foundation Layer (Model Integrity & Supply Chain) |
| **[MITRE ATLAS](https://atlas.mitre.org/matrices/ATLAS)** | [AML.TA0000](https://atlas.mitre.org/tactics/AML.TA0000) | Initial Access |
| **[MITRE ATLAS](https://atlas.mitre.org/matrices/ATLAS)** | [AML.T0018](https://atlas.mitre.org/techniques/AML.T0018) | Backdoor ML Model |
| **[MITRE ATT&CK](https://attack.mitre.org/)** | [TA0001](https://attack.mitre.org/tactics/TA0001/) | Initial Access |
| **[MITRE ATT&CK](https://attack.mitre.org/)** | [T1195.002](https://attack.mitre.org/techniques/T1195/002/) | Supply Chain Compromise: Compromise Software Supply Chain |
| **[MITRE CAPEC](https://capec.mitre.org/)** | [CAPEC-438](https://capec.mitre.org/data/definitions/438.html) | Modification During Manufacture |
| **[MITRE CAPEC](https://capec.mitre.org/)** | [CAPEC-441](https://capec.mitre.org/data/definitions/441.html) | Malicious Logic Insertion |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-494](https://cwe.mitre.org/data/definitions/494.html) | Download of Code Without Integrity Check |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-502](https://cwe.mitre.org/data/definitions/502.html) | Deserialization of Untrusted Data |
| **[NIST AI 100-2 E2023](https://doi.org/10.6028/NIST.AI.100-2e2023)** | [3.1](https://doi.org/10.6028/NIST.AI.100-2e2023) | Data Poisoning in Fine-Tuning |
| **[NIST AI 100-2 E2025](https://doi.org/10.6028/NIST.AI.100-2e2025)** | [NISTAML.010:2025](https://doi.org/10.6028/NIST.AI.100-2e2025) | Data Poisoning |
| **[OWASP Top 10](https://owasp.org/www-project-top-ten/)** | [A08:2021](https://owasp.org/Top10/2021/A08_2021-Software_and_Data_Integrity_Failures/) | Software and Data Integrity Failures |
| **[OWASP Top 10 2025](https://top10.owasp.org/2025/)** | [A08:2025](https://top10.owasp.org/2025/A08_2025-Software_or_Data_Integrity_Failures) | Software or Data Integrity Failures |
| **[OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** | [ASI07:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Insecure Inter-Agent Communication |
| **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** | [LLM03:2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) | Supply Chain Vulnerabilities |
| **[OWASP Top 10 for LLM Applications 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)** | [LLM04:2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) | Supply Chain |
| **[OWASP Top 10 for LLM Applications 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)** | [LLM05:2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) | Data and Model Poisoning |
