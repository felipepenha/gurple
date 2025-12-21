# <span style="color:var(--aurora)">**Introduction**</span>

GenAI has graduated from prototypes to production systems. This shift demands new security protocols. This chapter sets the stage for the content of the book by defining security roles and identifying the specific attack entry points for Threats to GenAI systems.


<br />

---
# 🌈 **Rainbow of Colors**

...


### **Black Hat Hackers**

...


### **White Hat and Ethical Hackers**

...


### **Red Teams**

...


### **Blue Teams**

...


### **Purple Teams**

* Validation: How to safely simulate this attack against the production defenses to prove they are working (e.g., specific evaluation test cases).


<br />

---
# **GenAI Attack Entry Points**

Production GenAI systems are complex applications with a broad attack surface that extends well beyond the foundational models. Attackers can exploit numerous entry points to introduce malicious inputs, manipulate context, or compromise infrastructure. These vectors range from direct interactions and API endpoints to less obvious channels like supply chain dependencies and observability data:

- UI inputs: Forms, prompts, documents, code, feedback, etc.
- API endpoints: Forms, prompts, documents, code, feedback, etc.
- Sensor inputs: Images, videos, audio, etc.
- Indirect inputs: Data retrieved from external sources (e.g., websites, emails) that may contain hidden malicious content.
- Model Context Protocol (MCP) server and tools.
- Agent2Agent Protocol (A2A).
- Supply Chain: Operating system, libraries, packages, models, etc.
- Cache and persistent storage: Databases, file systems, etc.
- Observability integrations, e.g. via OpenTelemetry Protocol (OTLP).