<div style="text-align: center; color:var(--aurora)">
  <h1 style="color:var(--aurora); font-size: 3em; font-weight: bold;">Preface</h1>
</div>

!!! note
    Gurple focuses on <span style="color:var(--constellation)">**Security of GenAI systems**</span> rather than GenAI-Assisted Security of traditional systems.

!!! warning
    Gurple is a <span style="color:var(--sun)">**White Hat**</span> and <span style="color:var(--sun)">**Ethical Hacking**</span> guidebook, meaning that it is NOT intended to be used for malicious purposes.

    Follow these principles:

    - **Obtain Authorization:** Ensure you have explicit, written permission from the system owner before performing any security testing.
    - **Stay within Scope:** Run tests strictly within agreed-upon boundaries and sandbox environments; never test against production systems without authorization.
    - **Legal Compliance:** Comply with all applicable laws and regulations regarding cybersecurity and data privacy.
    - **Defensive Intent:** Apply these methods solely to identify vulnerabilities and improve the security posture of GenAI systems.
    - **No Liability:** The authors are not responsible for any misuse of this information or damage caused by unauthorized testing.

    Just because you can do something, it doesn’t mean you should!


<br />

---
# **Gurple**

```python3

      /$$$$$$  /$$   /$$ /$$$$$$$  /$$$$$$$  /$$       /$$$$$$$$
     /$$__  $$| $$  | $$| $$__  $$| $$__  $$| $$      | $$_____/
    | $$  \__/| $$  | $$| $$  \ $$| $$  \ $$| $$      | $$      
    | $$ /$$$$| $$  | $$| $$$$$$$/| $$$$$$$/| $$      | $$$$$   
    | $$|_  $$| $$  | $$| $$__  $$| $$____/ | $$      | $$__/   
    | $$  \ $$| $$  | $$| $$  \ $$| $$      | $$      | $$      
    |  $$$$$$/|  $$$$$$/| $$  | $$| $$      | $$$$$$$$| $$$$$$$$
     \______/  \______/ |__/  |__/|__/      |________/|________/
                                                                
```

A wordplay on GenAI (letter "G") and "Purple Team" fused to become "Gurple".

At the same time, **gurple** is a mysterious and unusual color which is a mix of green and purple.

That's it! Just a book about GenAI Security and Purple Teaming, with a fun and memorable name.


<br />

---
# **Purpose**


## **GenAI Security vs. GenAI Safety**

Gurple focuses on **GenAI Security** rather than GenAI Safety.

**GenAI Security** and **GenAI Safety** are two distinct disciplines that frequently intersect. Safety generally targets unintentional failures, such as bias or hallucination, ensuring the system aligns with human intent. Security focuses on intentional malice, protecting the system from theft, disruption, or subversion. The boundary blurs when malicious actors weaponize safety failures or exploit security gaps to force unsafe outputs.

Adversarial attacks demonstrate this connection. A successful jailbreak is technically a security breach because it bypasses established access controls. The result is often a safety violation, such as the generation of instructions for illegal acts or hate speech. In this context, the security vulnerability serves as the vector for the safety failure. Defending against these attacks requires techniques from both fields.


## **Beyond Foundational Models and Towards Production-Grade GenAI**

Gurple moves beyond the typical focus on Foundational Models. Academic research often concentrates on model weights, steering or fine-tuning, yet production-grade GenAI exists within complex software systems. This approach addresses vulnerabilities in the models alongside the surrounding infrastructure which provides it with the means to communicate with the external world (UI, API endpoints, etc).

See [Attack Entry Points](../attack_entry_points/index.md) section to have a better understanding of the "doors" which attackers can use to exploit GenAI Systems.


## **Focus on Threats**

Gurple centers its analysis on [Threats](../threats/index.md) to GenAI systems, using the [`SCF C|P-RMM`](../threat_vulnerability_risk/scf_cp_rmm.md) framework to distinguish them from **Vulnerabilities** and **Risks**. For instance, **Prompt Injection** is treated as a distinct **Threat** that exploits system **Vulnerabilities** (such as Improper Output Handling) to introduce specific **Risks** (like malware generation), ensuring a clear separation of concerns.


## **Mapping to Popular Frameworks**

Gurple explains each of the most popular **Threat, Vulnerability and Risk** frameworks, and maps each of the **Threats** listed in this book to these frameworks by referencing unique IDs. While any attempt to map is imperfect, Gruple's map tables provide a quick way to navigate between frameworks and allows for more in-depth study of each threat. For example, Prompt Injection / Exfiltration Through Deserialization is mapped to [OWASP LLM02:2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/), giving the reader a broader idea of Deserialization of Untrusted Data beyond just GenAI. A mapping as extensive as this is certainly unique content not found anywhere else in the literature.


## **The Purple Team Approach**

Existing literature usually addresses Red Teaming (offense) and Blue Teaming (defense) separately. Gurple integrates them into a Purple strategy. This approach treats offense and defense as interconnected components, creating a feedback loop where attacks directly verify the efficacy of security controls.


## **Extensive Literature and Tech Stack Review**

Gurple is, at the same time, grounded in reality and in the literature, be it academic research papers, books, case studies, whitepapers, or industry reports. It provides analysis of real-world **Threats** to GenAI systems, with their proper references.

Gurple provides an up to date list of the available tech stack wherever it makes sense, usually linking to the GitHub repositories of the tools, documentation, and/or academic papers. "Up to date", here, means "up to date at the time of writing".

Readers are encouraged to suggest updates to the lists of references and technologies by opening new tickets at the [GitHub Issues Page](https://github.com/felipepenha/gurple/issues).

You will see a _References_ section at the end of each page.


<br />

---
# **Content**

**Gurple** explores GenAI Security by isolating individual **Threats** to GenAI systems and providing for each:

* In-depth information, including mapping to other frameworks and references from existing literature.

* Examples and case studies.

* Ethical Hacking and White Hat methodology:

    * Red Team: Steps to exploit.

    * Blue Team: Steps to detect and mitigate.

And, by the way, what's up with all these hat and team colors? Please, see the [Introduction](../introduction/index.md) for a detailed explanation.

See, next, how the main chapter of this book, the [Threat](../threats/index.md) chapter, is structured.


<br />

---
# **Structure of the _Threats_ Chapter**

# <span style="color:var(--aurora)">**[Section or Subsection Name]**</span>

# **Description**

A short description of the threat.

# **Map**

Maps the Gurple ID to various other IDs found in different GenAI threats and vulnerabilities frameworks.

| **Framework** | **ID** | **Title** |
| --- | --- | --- |
| **Gurple** | G.x.y | Description |
| **A** | A001 | Description |
| **B** | B001 | Description |

Gurple's Threat IDs follow the pattern `G-e.x.y`, which implies the following hierarchy:

* `e`: book edition number.
* `x`: Threat Type (section) number.
* `y`: Threat Subtype (subsection) number.

The order of the IDs is not significant, and reflects simply the order in which the sections were written.

# **Mechanism**

Describes the mechanism of the threat.

## **Attack Entry Points**

Basically, any Entry Point where a serialized object could be passed on to the system, even if disguised as regular text or data, to be later deserialized.

* [ ] **The Front Door** 🚪 — **Network & Application Interfaces**
    * [ ] **Application Programming Interface (API) Endpoints**
    * [ ] **User Interface (UI)**
    * [ ] **Sensors**

    _Note: Nothing really prevents an attacker from writing a serialized object on a sign or a t-shirt and presenting it to a camera, or dictating it to a voice-activated assistant._

    * [ ] **Observability Integration Interfaces**
* [ ] **The Side Door** 🚪 — **Supply Chain**

    _Note: Exploitation of deserialization vulnerabilities in dependencies._

* [ ] **The Back Door** 🚪 — **Data Storage**
* [ ] **The Hidden Door** 🚪 — **Event-Driven & Serverless Triggers**
    * [ ] **Indirect Sources**
    * [ ] **Agentic Tools**
    * [ ] **Model Context Protocol (MCP)**
    * [ ] **Agent2Agent Protocol (A2A)**
    * [ ] **Infrastructure Events**

# **Impact**

Explains the impact of the threat.

## **System Impact**

How it impacts the system.

## **Business Impact**

How it impacts the business.

### **Financial Impact**

### **Legal Impact**

### **Operational Impact**

### **Regulatory Impact**

### **Reputational Impact**

### **Etc ...**

# **Case Study** [if any]

Provides the summary and reference to a case study.


# 🔴 <span style="color:var(--red)">**Red Team**</span>

* Methodology: Steps to exploit.

* Example [if any]: Prompt or script.


# 🔵 <span style="color:var(--constellation)">**Blue Team**</span>

* Mitigation: Configuration changes, guardrails, or code fixes to prevent the attack.

* Detection: Logs, alerts, or keywords to monitor.

* Example [if any]: Prompt or script.