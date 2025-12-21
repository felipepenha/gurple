# <span style="color:var(--aurora)">**Preface**</span>

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

A wordplay on GenAI (letter "G") and "Purple Team" fused to become "Gurple".

At the same time, **gurple** is a mysterious and unusual color which is a mix of green and purple.

That's it! Just a book about GenAI Security with a fun and memorable name.


<br />

---
# **Purpose**


## **GenAI Security Vs. GenAI Safety**

Gurple focuses on **GenAI Security** rather than GenAI Safety.

**GenAI Security** and **GenAI Safety** are two distinct disciplines that frequently converge. Safety generally targets unintentional failures, such as bias or hallucination, ensuring the system aligns with human intent. Security focuses on intentional malice, protecting the system from theft, disruption, or subversion. The boundary blurs when malicious actors weaponize safety failures or exploit security gaps to force unsafe outputs.

Adversarial attacks demonstrate this connection. A successful jailbreak is technically a security breach because it bypasses established access controls. The result is often a safety violation, such as the generation of instructions for illegal acts or hate speech. In this context, the security vulnerability serves as the vector for the safety failure. Defending against these attacks requires techniques from both fields.


## **Beyond Foundational Models**

Gurple moves beyond the typical focus on Foundational Models. Research often concentrates on model weights, steering or fine-tuning, yet production GenAI exists within complex software systems. This approach addresses vulnerabilities in the model alongside the surrounding infrastructure, including API endpoints, MCP servers, A2A protocols, memory caching, persistent databases, and other components.

See [Introduction / GenAI Attack Entry Points](../introduction/index.md#genai-attack-entry-points) section for more details.


## **The Purple Team Approach**

Existing academic literature usually addresses Red Teaming (offense) and Blue Teaming (defense) separately. Gurple integrates them into a Purple strategy. This approach treats offense and defense as interconnected components, creating a feedback loop where attacks directly verify the efficacy of security controls.

<br />

---
# **Content**

**Gurple** explores GenAI Security by isolating individual **Threats** to GenAI systems and providing for each:

* In-depth information, including references from existing literature.

* Examples and case studies.

* Ethical Hacking and White Hat methodology:

    * Red Team: Steps to exploit.

    * Blue Team: Steps to detect and mitigate.

    * Purple Team: Steps to verify.

You will have a better understanding of what **Threats** are in the [Threat, Vulnerability & Risk Frameworks](../threat_vulnerability_frameworks/index.md) chapter, primarily by studying the [C|P-RMM](https://cp-rmm.com) framework.

And, by the way, what's up with all these hat and team colors? Please, see the [Introduction](../introduction/index.md) for a detailed explanation.


<br />

---
# **Structure of the _Threat_ Chapter**

# <span style="color:var(--aurora)">**[G-e.x.y] &mdash; [Section Name]**</span>

Threat chapter's sections and subsections are numbered based on custom threat IDs of the form `G-e.x.y`, to facilitate referrencing these later.

The IDs imply a hierarchy:

* `e`: book edition number.
* `x`: threat type (section) number.
* `y`: threat (subsection) number.

The order of the IDs is not significant, and reflects simply the order in which the sections were written.

## **Map**

Maps the Gurple ID to various other IDs found in different GenAI threats and vulnerabilities frameworks.

| **Framework** | **ID** | **Title** |
| --- | --- | --- |
| **Gurple** | G.x.y | Description |
| **A** | A001 | Description |
| **B** | B001 | Description |


## **Mechanism**

Describes the mechanism of the threat.


## **Impact**

Explains the impact of the threat.


## **Case Study** [if any]

Provides the summary and reference to a case study.


## 🔴 <span style="color:var(--red)">**Red Team**</span>

* Methodology: Steps to exploit.

* Example [if any]: Prompt or script.


## 🔵 <span style="color:var(--constellation)">**Blue Team**</span>

* Mitigation: Configuration changes, guardrails, or code fixes to prevent the attack.

* Detection: Logs, alerts, or keywords to monitor.

* Example [if any]: Prompt or script.


## **References**

1. ...
2. ...
3. ...
