# <span style="color:var(--aurora)">**Exfiltration Through Deserialization**</span>

------------------------------------------------------------------------

# **Description**

Deserialization of untrusted data occurs when an application deserializes data from an untrusted source without sufficient validation. In the context of GenAI, this vulnerability can be exploited when the model processes serialized objects (e.g., `JSON`, `pickle`, `joblib`) [[1]](#ref-NIST:AI:100-2e2023) provided via prompts or attached data. Specifically for **Exfiltration**, the adversarial prompt is designed to coerce the system into reading sensitive data from the system’s environment or filesystem (e.g., API keys, user credentials) and transmitting it back as chat answers or logs that may be further exploited.

<br />

------------------------------------------------------------------------

# **Map**

| **Framework**                                                                                                        | **ID**                                                                                  | **Title**                                                                                        |
|----------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| **[Gurple](https://felipepenha.github.io/gurple/threats/)**                                                          | G-1.1.1                                                                                 | Prompt Injection & Exfiltration Through Deserialization                                          |
| **[MITRE ATLAS](https://atlas.mitre.org/matrices/ATLAS)**                                                            | [AML.TA0010](https://atlas.mitre.org/tactics/AML.TA0010)                                | Exfiltration                                                                                     |
| **[MITRE ATT&CK](https://attack.mitre.org/)**                                                                        | [TA0010](https://attack.mitre.org/tactics/TA0010/)                                      | Exfiltration                                                                                     |
| **[MITRE CWE](https://cwe.mitre.org/)**                                                                              | [CWE-502](https://cwe.mitre.org/data/definitions/502.html)                              | Deserialization of Untrusted Data                                                                |
| **[OWASP Top 10](https://owasp.org/www-project-top-ten/)**                                                           | [A08:2021](https://owasp.org/Top10/2021/A08_2021-Software_and_Data_Integrity_Failures/) | Software and Data Integrity Failures                                                             |
| **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** | [LLM02:2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)  | Sensitive Information Disclosure                                                                 |
| **[SCF C\|P-RMM](https://securecontrolsframework.com/free/risk-management-model/)**                                  | [R-BC-4](https://securecontrolsframework.com/free/risk-management-model/)               | Business Continuity & Information loss / corruption or system compromise due to technical attack |

<br />

------------------------------------------------------------------------

# **Mechanism**

Starting from a safe serialized object in the expected format, the attacker performs a malicious edition that will pass unnoticed through the deserialization process. The object is, then, included in the user input to the GenAI system (e.g., user prompts, forms, attached data).

<p align="center" markdown="1">
<img src="../images/CWE-502-Diagram.png" alt="CWE-502 Deserialization Diagram" />
<br />
<em>Figure 1: Deserialization of Untrusted Data [[2]](#ref-MITRE:CWE502:Deserialization).</em>
</p>

To result in **Exfiltration**, the payload is specifically engineered to output information from files (e.g., `/etc/passwd`, `.env` files), databases, or environment variables.

## **Attack Entry Points**

Basically, any Entry Point where a serialized object could be passed on to the system, even if disguised as regular text or data, to be later deserialized.

-   [x] **The Front Door** 🚪 — **Network & Application Interfaces**

    -   [x] **Application Programming Interface (API) Endpoints**

    -   [x] **User Interface (UI)**

    -   [x] **Sensors**

        *Note: Nothing really prevents an attacker from writing a serialized object on a sign or a t-shirt and presenting it to a camera, or dictating it to a voice-activated assistant.*

    -   [ ] **Observability Integration Interfaces**

-   [x] **The Side Door** 🚪 — **Supply Chain**

    *Note: Exploitation of deserialization vulnerabilities in dependencies.*

-   [x] **The Back Door** 🚪 — **Data Storage**

-   [x] **The Hidden Door** 🚪 — **Event-Driven & Serverless Triggers**

    -   [x] **Indirect Sources**
    -   [x] **Agentic Tools**
    -   [x] **Model Context Protocol (MCP)**
    -   [x] **Agent2Agent Protocol (A2A)**
    -   [x] **Infrastructure Events**

<br />

------------------------------------------------------------------------

# **Impact**

## **System Impact**

No direct and immediate impact on the system. The deserialization vulnerability can be exploited to exfiltrate sensitive information from the system, but it does not directly impact the system’s functionality or performance.

Note, however, that the exfiltrated information can include keys to decode encrypted data, and may be used to exploit the system further.

## **Business Impact**

Sensitive information is exfiltrated from the system, impacting Business Continuity. The exfiltrated information can include secrets to access other services (e.g. APIs, databases), user credentials, or other sensitive data.

### **Financial Impact**

Financial impact may be caused by gaining access to financial data, such as credit card numbers, bank account numbers, or other sensitive information. Alternatively, the attacker may harvest resources by gaining access to the integrated services via the exfiltrated secrets.

### **Legal Impact**

Legal impact may be caused by users seeking compensation for the loss of data, or other damages resulting from the attack.

### **Operational Impact**

Operational impact may be caused by the need to shut down systems for urgent remediation (e.g., rotating compromised secrets/keys).

### **Regulatory Impact**

Regulatory impact may be caused by non-compliance to regulations, such as GDPR, HIPAA, or PCI DSS. This can result in fines, legal action, or other penalties.

### **Reputational Impact**

Reputational impact may be caused by the hackers exposing the successful attack to the public, and / or by leaking sensitive information.

<br />

------------------------------------------------------------------------

# **Case Study**

## **LangGrinch**

LangGrinch [[3]](#ref-Cyata:LangGrinch:WEB) [[4]](#ref-CybersecurityNews:LangGrinch:WEB) [[5]](#ref-TheHackerNews:LangGrinch:WEB) [[6]](#ref-WebProNews:LangGrinch:WEB) is a vulnerability that has already been reported and resolved. There are no known reports of successful attacks impacting businesses. Therefore, this case study is for illustrative purposes only.

Reported vulnerabilities:

| **Vulnerability IDs**                                                                                                                                | **Description**                                                                               |
|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| \- [CVE-2025-68664](https://nvd.nist.gov/vuln/detail/CVE-2025-68664)<br />- [GHSA-c67j-w6g6-q2cm](https://github.com/advisories/GHSA-c67j-w6g6-q2cm) | LangChain serialization injection vulnerability enables secret extraction in dumps/loads APIs |
| \- [CVE-2025-68665](https://nvd.nist.gov/vuln/detail/CVE-2025-68665)<br />- [GHSA-r399-636x-v7f6](https://github.com/advisories/GHSA-r399-636x-v7f6) | LangChain serialization injection vulnerability enables secret extraction                     |

Additional mapping, for this specific case study:

| **Framework**                                                                                                        | **ID**                                                                                  | **Title**                                                       |
|----------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| **[MITRE ATLAS](https://atlas.mitre.org/matrices/ATLAS)**                                                            | [AML.T0010](https://atlas.mitre.org/techniques/AML.T0010)                               | AI Supply Chain Compromise                                      |
| **[MITRE ATT&CK](https://attack.mitre.org/)**                                                                        | [T1195](https://attack.mitre.org/techniques/T1195/)                                     | Supply Chain Compromise                                         |
| **[MITRE CWE](https://cwe.mitre.org/)**                                                                              | [CWE-1357](https://cwe.mitre.org/data/definitions/1357.html)                            | Reliance on Insufficiently Trustworthy Component                |
| **[NIST AI 100-2 E2023](https://doi.org/10.6028/NIST.AI.100-2e2023)**                                                | [3.2](https://doi.org/10.6028/NIST.AI.100-2e2023)                                       | AI Supply Chain Attacks and Mitigations                         |
| **[NIST AI 100-2 E2023](https://doi.org/10.6028/NIST.AI.100-2e2023)**                                                | [3.2.1](https://doi.org/10.6028/NIST.AI.100-2e2023)                                     | Deserialization Vulnerability                                   |
| **[OWASP Top 10](https://owasp.org/www-project-top-ten/)**                                                           | [A06:2021](https://owasp.org/Top10/2021/A08_2021-Software_and_Data_Integrity_Failures/) | Vulnerable and Outdated Components                              |
| **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** | [LLM03:2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)  | Supply Chain                                                    |
| **[SCF C\|P-RMM](https://securecontrolsframework.com/free/risk-management-model/)**                                  | [R-SC-3](https://securecontrolsframework.com/free/risk-management-model/)               | Third-party supply chain relationships, visibility and controls |

An attack based on LangGrinch would

<br />

------------------------------------------------------------------------

# 🔴 <span style="color:var(--red)">**Red Team**</span>

-   Methodology: Steps to exploit.

-   Example [if any]: Prompt or script.

<br />

------------------------------------------------------------------------

# 🔵 <span style="color:var(--constellation)">**Blue Team**</span>

-   Mitigation: Configuration changes, guardrails, or code fixes to prevent the attack.

-   Detection: Logs, alerts, or keywords to monitor.

-   Example [if any]: Prompt or script.

<br />

---

# References

<div id="refs" class="references csl-bib-body">

<div id="ref-NIST:AI:100-2e2023" class="csl-entry">

<span class="csl-left-margin">[1] </span><span class="csl-right-inline">A. Vassilev, A. Oprea, A. Fordyce, and H. Anderson, “Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations,” National Institute of Standards and Technology, NIST Artificial Intelligence (AI) 100-2 E2023, Jan. 2024. doi: <a href="https://doi.org/10.6028/NIST.AI.100-2e2023">10.6028/NIST.AI.100-2e2023</a>.</span>

</div>

<br />

<div id="ref-MITRE:CWE502:Deserialization" class="csl-entry">

<span class="csl-left-margin">[2] </span><span class="csl-right-inline">“CWE - CWE-502: Deserialization of Untrusted Data (4.19).” <a href="https://cwe.mitre.org/data/definitions/502.html">https://cwe.mitre.org/data/definitions/502.html</a>.</span>

</div>

<br />

<div id="ref-Cyata:LangGrinch:WEB" class="csl-entry">

<span class="csl-left-margin">[3] </span><span class="csl-right-inline">P. Yarden, “All I Want for Christmas is Your Secrets: LangGrinch hits LangChain Core (CVE-2025-68664),” <em>Cyata  The Control Plane for Agentic Identity</em>. <a href="https://cyata.ai/blog/langgrinch-langchain-core-cve-2025-68664/">https://cyata.ai/blog/langgrinch-langchain-core-cve-2025-68664/</a>, Dec. 2025.</span>

</div>

<br />

<div id="ref-CybersecurityNews:LangGrinch:WEB" class="csl-entry">

<span class="csl-left-margin">[4] </span><span class="csl-right-inline">G. Baran, “Critical Langchain Vulnerability Let attackers Exfiltrate Sensitive Secrets from AI systems,” <em>Cyber Security News</em>. <a href="https://cybersecuritynews.com/langchain-vulnerability/">https://cybersecuritynews.com/langchain-vulnerability/</a>, Dec. 2025.</span>

</div>

<br />

<div id="ref-TheHackerNews:LangGrinch:WEB" class="csl-entry">

<span class="csl-left-margin">[5] </span><span class="csl-right-inline">R. Lakshmanan, “Critical LangChain Core Vulnerability Exposes Secrets via Serialization Injection,” <em>The Hacker News</em>. <a href="https://thehackernews.com/2025/12/critical-langchain-core-vulnerability.html">https://thehackernews.com/2025/12/critical-langchain-core-vulnerability.html</a>.</span>

</div>

<br />

<div id="ref-WebProNews:LangGrinch:WEB" class="csl-entry">

<span class="csl-left-margin">[6] </span><span class="csl-right-inline">E. Hastings, “LangGrinch Vulnerability Exposes LangChain AI to Secret Theft Risks,” <em>WebProNews</em>. <a href="https://www.webpronews.com/langgrinch-vulnerability-exposes-langchain-ai-to-secret-theft-risks/">https://www.webpronews.com/langgrinch-vulnerability-exposes-langchain-ai-to-secret-theft-risks/</a>, Dec. 2025.</span>

</div>

<br />

</div>
