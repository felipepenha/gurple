# <span style="color:var(--aurora)">**Attack Entry Points**</span>

Production GenAI systems are complex applications with a broad attack surface that extends well beyond the foundational models. Attackers can exploit numerous entry points to introduce malicious inputs, manipulate context, or compromise infrastructure. These vectors range from direct interactions via the User Interface (UI) and Application Programming Interface (API) endpoints to less obvious channels like supply chain dependencies and integrations to observability software:


## **User Interface (UI)**

Attackers may input data via the UI, which is then processed by the GenAI system.

Examples of data: forms, prompts, documents, code, feedback, images, videos, audio, etc.


## **Application Programming Interface (API) Endpoints**
    
Attackers may input data via the application's API endpoints, which is then processed by the GenAI system.

Examples of data: forms, prompts, documents, code, feedback, images, videos, audio, etc.


## **Sensors**

Attackers may present malicious signals to sensors such as cameras and microphones, which is then processed by the GenAI system.

Examples of malicious signals: noise, going beyond the sensor's range, evading identification,inducing misclassification, etc.


## **Indirect Sources**

Data retrieved from indirect sources that may contain hidden malicious content.

Examples of indirect sources: websites, emails, code versioning repositories, etc.


## **Agentic Tools**

External tools that perform actions on behalf of agents.

Examples of tools: executes code, sends email, etc.


## **Model Context Protocol (MCP)**

Attackers may exploit the MCP client or the MCP server, e.g. to inject malicious context into the model.


## **Agent2Agent Protocol (A2A)**

Attackers may exploit the A2A client or the A2A server, e.g. to intercept or manipulate communications between autonomous agents.


## **Supply Chain**

Attackers may compromise the foundational components upon which the GenAI system is built.

Examples of components: models, libraries, packages container images, etc.


## **Cache and Persistent Storage**

Attackers may poison or compromise the data storage that the model accesses.

Examples of data storage: cache databases for memory, persistent databases for logging conversation history and feedback, persistent vector databases for semantic search, etc.


## **Observability Integration Protocols**

Attackers may target the observability integration protocols to blind defenders or exfiltrate information.

Examples of integration protocols: OpenTelemetry (OTel), HTTPS, etc.
