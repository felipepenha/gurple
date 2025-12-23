<div style="text-align: center; color:var(--aurora)">
  <p style="font-size: 8em; margin-top: 0px; margin-bottom: 0px; font-weight: bold;">2</p>
  <h1 style="color:var(--aurora); font-size: 3em; font-weight: bold;">Attack Entry Points</h1>
</div>

Production GenAI systems are complex applications with a broad Attack Surface that extends well beyond the GenAI models. Attackers can exploit numerous entry points to introduce malicious inputs, manipulate context, or compromise infrastructure.


<br />

---
# **The Front Door** 🚪 <br /> **&mdash; Network & Application Interfaces**

These are the primary interaction points where the system accepts multimodal input for inference.

<br />

* **Application Programming Interface (API) Endpoints**

    Attackers may input data via the application's API endpoints, directly accessing the model or orchestration layer.

    **Examples of structured data:** structured data (JSON, XML, etc), inputs to forms (name, address, etc), feedback (thumbs up, thumbs down, etc).

    **Examples of unstructured data:** prompts, documents (PDF, Doc, etc), free text, images, videos, audio, code (SQL, Python, etc).

<br />
    
* **User Interface (UI)**

    Attackers may input either structured or unstructured data via the UI, which is then processed by the GenAI system.

    Examples for UI input data would be exactly the same as for API Endpoints, since UI interactions are ultimately translated into API calls.

<br />

* **Sensors**

    Attackers may present malicious signals to physical sensors (cameras, microphones, motion sensors, etc), which are then processed by the GenAI system.

    **Examples of malicious signals:** noise (adversarial examples), signals going beyond the sensor's range, evading identification, inducing misclassification.

<br />

* **Observability Integration Interfaces**

    Attackers may target the observability integration protocols to blind defenders or exfiltrate sensitive model inputs/outputs.

    **Examples of integration protocols:** OpenTelemetry (OTel), HTTPS logging streams.

<br />

---
# **The Side Door** 🚪 <br /> **&mdash; Supply Chain**

Attackers may compromise the foundational components upon which the GenAI system is built to introduce backdoors or bias. Supply chain attacks often bypass traditional perimeter defenses because the compromised component is invited inside the trusted environment by the developers themselves.

**Examples of components:** model files, system libraries, packages, container images, codebase hosted in code version control platforms.

<br />


---
# **The Back Door** 🚪 <br /> **&mdash; Data Storage**

In GenAI systems, data storage form the basis for functional aspects, such as Memory and Knowledge Base. It differs from traditional systems in that it is not only used for directly retrieving information to be displayed to the user, but also for retrieving context for the model layer.

**Examples of data storage:** Cache databases for session memory, persistent databases for logging conversation history, persistent vector databases for semantic search, cloud storage with raw data.

<br />

---
# **The Hidden Door** 🚪 <br /> **&mdash; Event-Driven & Serverless Triggers**

GenAI agents often act autonomously based on external triggers or indirect data, creating invisible entry points.

<br />

* **Indirect Sources**

    Data retrieved from indirect sources that may contain hidden malicious content (Indirect Prompt Injection).

    **Examples of indirect sources:** scraped websites, ingested emails, reviewed code.

<br />

* **Agentic Tools**

    External tools that perform actions on behalf of agents. Attackers may exploit the tool's output to hijack the agent's control flow.

    **Examples of tools:** code execution sandboxes, email sending APIs, file system access tools.

<br />

* **Model Context Protocol (MCP)**

    Attackers may exploit the MCP client or the MCP server.

    **Examples of vectors:** Injecting malicious context into the model, manipulating context handover.

<br />

* **Agent2Agent Protocol (A2A)**

    Attackers may exploit the A2A client or the A2A server.

    **Examples of vectors:** Intercepting or manipulating communications between autonomous agents.

<br />

* **Infrastructure Events**

    Attackers may trigger GenAI processing pipelines via backend events.

    **Examples of events:** File upload triggers (initiating embedding generation), Message Queue injection (forcing the model to process a malicious payload).