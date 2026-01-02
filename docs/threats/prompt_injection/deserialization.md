# <span style="color:var(--aurora)">**Exfiltration Through Deserialization**</span>

---
# **Description**

Deserialization of untrusted data occurs when an application deserializes data from an untrusted source without sufficient validation. In the context of GenAI, this vulnerability can be exploited when the model processes serialized objects (e.g., `JSON`, `pickle`) provided via prompts or attached data. Specifically for **Exfiltration**, the adversarial prompt is designed to coerce the system into reading sensitive data from the system's environment or filesystem (e.g., API keys, user credentials) and transmitting it back as chat answers or logs that may be further exploited.

<br />

---
# **Map**

| **Framework** | **ID** | **Title** |
| --- | --- | --- |
| **[Gurple](https://felipepenha.github.io/gurple/threats/)** | G-1.1.1 | Prompt Injection & Exfiltration Through Deserialization |
| **[MITRE ATLAS](https://atlas.mitre.org/matrices/ATLAS)** | [AML.TA0010](https://atlas.mitre.org/tactics/AML.TA0010) | Exfiltration |
| **[MITRE ATT&CK](https://attack.mitre.org/)** | [TA0010](https://attack.mitre.org/tactics/TA0010/) | Exfiltration |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-502](https://cwe.mitre.org/data/definitions/502.html) | Deserialization of Untrusted Data |
| **[OWASP Top 10](https://owasp.org/www-project-top-ten/)** | [A08:2021](https://owasp.org/Top10/2021/A08_2021-Software_and_Data_Integrity_Failures/) | Software and Data Integrity Failures |
| **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** | [LLM02:2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) | Sensitive Information Disclosure |
| **[SCF C\|P-RMM](https://securecontrolsframework.com/free/risk-management-model/)** | [R-BC-4](https://securecontrolsframework.com/free/risk-management-model/) | Business Continuity & Information loss / corruption or system compromise due to technical attack |


<br />

---
# **Mechanism**

Starting from a safe serialized object in the expected format, the attacker performs a malicious edition that will pass unnoticed through the deserialization process. The object is, then, included in the user input to the GenAI system (e.g., user prompts, forms, attached data).

<p align="center">
  <img src="../images/CWE-502-Diagram.png" alt="CWE-502 Deserialization Diagram" />
  <br />
  <em>Figure 1: Deserialization of Untrusted Data [@CWE502:Deserialization].</em>
</p>

To result in **Exfiltration**, the payload is specifically engineered to output information from files (e.g., `/etc/passwd`, `.env` files), databases, or environment variables.

## **Attack Entry Points**

Basically, any Entry Point where a serialized object could be passed on to the system, even if disguised as regular text or data, to be later deserialized.

* [x] **The Front Door** 🚪 — **Network & Application Interfaces**
    * [x] **Application Programming Interface (API) Endpoints**
    * [x] **User Interface (UI)**
    * [x] **Sensors**

    _Note: Nothing really prevents an attacker from writing a serialized object on a sign or a t-shirt and presenting it to a camera, or dictating it to a voice-activated assistant._

    * [ ] **Observability Integration Interfaces**
* [x] **The Side Door** 🚪 — **Supply Chain**

    _Note: Exploitation of deserialization vulnerabilities in dependencies._

* [x] **The Back Door** 🚪 — **Data Storage**
* [x] **The Hidden Door** 🚪 — **Event-Driven & Serverless Triggers**
    * [x] **Indirect Sources**
    * [x] **Agentic Tools**
    * [x] **Model Context Protocol (MCP)**
    * [x] **Agent2Agent Protocol (A2A)**
    * [x] **Infrastructure Events**


<br />

---
# **Impact**


## **System Impact**

No direct and immediate impact on the system. The deserialization vulnerability can be exploited to exfiltrate sensitive information from the system, but it does not directly impact the system's functionality or performance.

Note, however, that the exfiltrated information can include keys to decode encrypted data, and may be used to exploit the system further.


## **Business Impact**

Sensitive information is exfiltrated from the system, impacting Business Continuity. The exfiltrated information can include secrets to access other services (e.g. APIs, databases), user credentials, or other sensitive data.

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

---
# **Case Study**

## **LangGrinch**

LangGrinch is a vulnerability that has already been reported and resolved. There are no known reports of successful attacks impacting businesses. Therefore, this case study is for illustrative purposes only.

Reported vulnerabilities:

| **Vulnerability ID** | **Description** | **References** |
| --- | --- | --- |
[CVE-2025-68664](https://nvd.nist.gov/vuln/detail/CVE-2025-68664) | LangChain serialization injection vulnerability enables secret extraction in dumps/loads APIs | [GHSA-c67j-w6g6-q2cm](https://github.com/advisories/GHSA-c67j-w6g6-q2cm)<br />[CVE-2025-68664](https://nvd.nist.gov/vuln/detail/CVE-2025-68664) |
[CVE-2025-68665](https://nvd.nist.gov/vuln/detail/CVE-2025-68665) | LangChain serialization injection vulnerability enables secret extraction | [GHSA-r399-636x-v7f6](https://github.com/advisories/GHSA-r399-636x-v7f6)<br />[CVE-2025-68665](https://nvd.nist.gov/vuln/detail/CVE-2025-68665) |

Additional mapping, for this specific case study:

| **Framework** | **ID** | **Title** |
| --- | --- | --- |
| **[MITRE ATLAS](https://atlas.mitre.org/matrices/ATLAS)** | [AML.T0010](https://atlas.mitre.org/techniques/AML.T0010) | AI Supply Chain Compromise |
| **[MITRE ATT&CK](https://attack.mitre.org/)** | [T1195](https://attack.mitre.org/techniques/T1195/) | Supply Chain Compromise |
| **[MITRE CWE](https://cwe.mitre.org/)** | [CWE-1357](https://cwe.mitre.org/data/definitions/1357.html) | Reliance on Insufficiently Trustworthy Component |
| **[NIST AI 100-2 E2023](https://doi.org/10.6028/NIST.AI.100-2e2023)** | [3.2](https://doi.org/10.6028/NIST.AI.100-2e2023) | AI Supply Chain Attacks and Mitigations |
| **[NIST AI 100-2 E2023](https://doi.org/10.6028/NIST.AI.100-2e2023)** | [3.2.1](https://doi.org/10.6028/NIST.AI.100-2e2023) | Deserialization Vulnerability |
| **[OWASP Top 10](https://owasp.org/www-project-top-ten/)** | [A06:2021](https://owasp.org/Top10/2021/A08_2021-Software_and_Data_Integrity_Failures/) | Vulnerable and Outdated Components |
| **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** | [LLM03:2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) | Supply Chain |
| **[SCF C\|P-RMM](https://securecontrolsframework.com/free/risk-management-model/)** | [R-SC-3](https://securecontrolsframework.com/free/risk-management-model/) | Third-party supply chain relationships, visibility and controls |


<br />

---
# 🔴 <span style="color:var(--red)">**Red Team**</span>

* Methodology: Steps to exploit.

* Example [if any]: Prompt or script.


<br />

---
# 🔵 <span style="color:var(--constellation)">**Blue Team**</span>

* Mitigation: Configuration changes, guardrails, or code fixes to prevent the attack.

* Detection: Logs, alerts, or keywords to monitor.

* Example [if any]: Prompt or script.