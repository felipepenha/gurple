<div style="text-align: center; color:var(--aurora)">

<p style="font-size: 8em; margin-top: 0px; margin-bottom: 0px; font-weight: bold;">
2
</p>
<h1 style="color:var(--aurora); font-size: 3em; font-weight: bold;">
Attack Entry Points
</h1>

</div>

Production GenAI systems are complex applications with a broad Attack Surface that extends well beyond the GenAI models. Attackers can exploit numerous entry points to introduce malicious inputs, manipulate context, or compromise infrastructure.

<br />

------------------------------------------------------------------------

# **The Front Door** 🚪 <br /> **— Network & Application Interfaces**

These are the primary interaction points where the system accepts multimodal input for inference.

<br />

-   **Application Programming Interface (API) Endpoints**

    Attackers may input data via the application’s API endpoints, directly accessing the model or orchestration layer.

    **Examples of structured data:** structured data (JSON, XML, etc), inputs to forms (name, address, etc), feedback (thumbs up, thumbs down, etc).

    **Examples of unstructured data:** prompts, documents (PDF, Doc, etc), free text, images, videos, audio, code (SQL, Python, etc).

    ``` mermaid
    graph LR
        Attacker(["<span style='color:#000'>Attacker</span>"]) -->|"Malicious Payload"| API["<span style='color:#000'>API Endpoint</span>"]
        API -->|"Payload"| Model["<span style='color:#000'>GenAI System</span>"]

        classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
        classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
        classDef blue fill:#e0e7ff,stroke:#5f6de9,stroke-width:2px,color:#000;

        class Attacker red;
        class API blue;
        class Model yellow;
    ```

<br />

-   **User Interface (UI)**

    Attackers may input either structured or unstructured data via the UI, which is then processed by the GenAI system.

    Examples for UI input data would be exactly the same as for API Endpoints, since UI interactions are ultimately translated into API calls.

    ``` mermaid
    graph LR
        Attacker(["<span style='color:#000'>Attacker</span>"]) -->|"Input"| UI["<span style='color:#000'>User Interface</span>"]
        UI -->|"API Call"| API["<span style='color:#000'>API Endpoint</span>"]
        API -->|"Payload"| Model["<span style='color:#000'>GenAI System</span>"]

        classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
        classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
        classDef blue fill:#e0e7ff,stroke:#5f6de9,stroke-width:2px,color:#000;

        class Attacker red;
        class UI,API blue;
        class Model yellow;
    ```

<br />

-   **Sensors**

    Attackers may present malicious signals to physical sensors (cameras, microphones, motion sensors, etc), which are then processed by the GenAI system.

    **Examples of malicious signals:** noise (adversarial examples), signals going beyond the sensor’s range, evading identification, inducing misclassification.

    ``` mermaid
    graph LR
        Attacker(["<span style='color:#000'>Attacker</span>"]) -->|"Adversarial Signal"| Sensor["<span style='color:#000'>Sensor</span>"]
        Sensor -->|"Digital Signal"| Model["<span style='color:#000'>GenAI System</span>"]

        classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
        classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
        classDef blue fill:#e0e7ff,stroke:#5f6de9,stroke-width:2px,color:#000;

        class Attacker red;
        class Sensor blue;
        class Model yellow;
    ```

<br />

-   **Observability Integration Interfaces**

    Attackers may target the observability integration protocols to blind defenders or exfiltrate sensitive model inputs/outputs.

    **Examples of integration protocols:** OpenTelemetry (OTel), HTTPS logging streams.

    ``` mermaid
    graph LR
        Attacker(["<span style='color:#000'>Attacker</span>"]) -.->|"Exploits/Blinds"| OTel["<span style='color:#000'>Observability System</span>"]
        System["<span style='color:#000'>GenAI System</span>"] -->|"Logs/Traces"| OTel
        OTel -->|"Feeds"| Dash["<span style='color:#000'>Dashboard</span>"]

        classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
        classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
        classDef blue fill:#e0e7ff,stroke:#5f6de9,stroke-width:2px,color:#000;
        classDef purple fill:#ffe1f5,stroke:#d946ef,stroke-width:2px,color:#000;

        class Attacker red;
        class System yellow;
        class OTel blue;
        class Dash purple;
    ```

<br />

------------------------------------------------------------------------

# **The Side Door** 🚪 <br /> **— Supply Chain**

Attackers may compromise the foundational components upon which the GenAI system is built to introduce backdoors or bias. Supply chain attacks often bypass traditional perimeter defenses because the compromised component is invited inside the trusted environment by the developers themselves.

**Examples of components:** model files, system libraries, packages, container images, codebase hosted in code version control platforms.

```mermaid
graph LR
    Attacker(["<span style='color:#000'>Attacker</span>"]) -->|"Compromises"| Comp["<span style='color:#000'>Component</span>"]
    Comp -->|"Enters"| Build["<span style='color:#000'>CI/CD Pipeline</span>"]
    Build -->|"Deploys"| Prod["<span style='color:#000'>Production<br />GenAI System</span>"]

    classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
    classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
    classDef blue fill:#e0e7ff,stroke:#5f6de9,stroke-width:2px,color:#000;

    class Attacker red;
    class Comp,Build blue;
    class Prod yellow;
```

<br />

------------------------------------------------------------------------

# **The Back Door** 🚪 <br /> **— Data Storage**

In GenAI systems, data storage forms the basis for functional aspects, such as Memory and Knowledge Base. Unlike traditional systems that query storage primarily to display output to users, GenAI architectures also query storage to construct context for the model layer.

**Examples of data storage:** Cache databases for session memory, persistent databases for logging conversation history, persistent vector databases for semantic search, cloud storage with raw data.

```mermaid
graph LR
    Attacker(["<span style='color:#000'>Attacker</span>"]) -->|"Compromises"| DB[("<span style='color:#000'>Database/RAG</span>")]
    DB -->|"Context Retrieval"| Model["<span style='color:#000'>GenAI System</span>"]

    classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
    classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
    classDef purple fill:#ffe1f5,stroke:#d946ef,stroke-width:2px,color:#000;

    class Attacker red;
    class DB purple;
    class Model yellow;
```

<br />

------------------------------------------------------------------------

# **The Hidden Door** 🚪 <br /> **— Event-Driven & Serverless Triggers**

GenAI agents often act autonomously based on external triggers or indirect data, creating invisible entry points.

<br />

-   **Indirect Sources**

    Data retrieved from indirect sources that may contain hidden malicious content.

    **Examples of indirect sources:** scraped websites, ingested emails, reviewed code.

    ``` mermaid
    graph LR
        Attacker(["<span style='color:#000'>Attacker</span>"]) -->|"Malicious Content"| Web["<span style='color:#000'>Website<br />Email<br />Code</span>"]
        Web -->|"Poisons"| AI["<span style='color:#000'>GenAI System</span>"]

        classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
        classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
        classDef blue fill:#e0e7ff,stroke:#5f6de9,stroke-width:2px,color:#000;

        class Attacker red;
        class Web blue;
        class AI yellow;
    ```

<br />

-   **Rules, Skills & Memory Files**

    Attackers may plant or tamper with instructions, operational skills, or persistent memory files loaded by autonomous agents, hijacking their reasoning loop and tool permissions without direct user interaction.

    **Examples of files:** workspace rules (`AGENTS.md`, `CLAUDE.md`), agent skills (`SKILL.md`), persistent memory files (`memory.json`, `MEMORY.md`), task history, project configurations.

    ``` mermaid
    graph TB
        Attacker(["<span style='color:#000'>Attacker</span>"]) -.->|"Poisons / Plants"| Files["<span style='color:#000'>Rules (AGENTS.md)<br />Skills (SKILL.md)<br />Memory (MEMORY.md)</span>"]
        Files -->|"Auto-Loaded into Context"| Agent["<span style='color:#000'>Autonomous Agent</span>"]
        Agent -->|"Compromised Execution"| Env["<span style='color:#000'>Workspace / Tools</span>"]

        classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
        classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
        classDef blue fill:#e0e7ff,stroke:#5f6de9,stroke-width:2px,color:#000;
        classDef purple fill:#ffe1f5,stroke:#d946ef,stroke-width:2px,color:#000;

        class Attacker red;
        class Files blue;
        class Agent yellow;
        class Env purple;
    ```

<br />

-   **Agentic Tools**

    Attackers may exploit the vulnerabilities of external tools that perform actions on behalf of agents, by providing malicious content (context and instructions) that hijack the agent’s control flow.

    **Examples of tools:** web search, web fetch, code execution, email, file system.

    ``` mermaid
    graph LR

        subgraph dashed_box ["GenAI System"]
            Agents["<span style='color:#000'>Agents</span>"]
            Tools["<span style='color:#000'>Tools</span>"]
        end

        Agents -->|"Multi-step<br />Tool Calling"| Tools
        Attacker(["<span style='color:#000'>Attacker</span>"]) -.->|"Malicious Context<br />Malicious Instructions"| Tools

        Tools -->|"Execute"| Tasks["<span style='color:#000'>Tasks</span>"]

        classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
        classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
        classDef blue fill:#e0e7ff,stroke:#5f6de9,stroke-width:2px,color:#000;
        classDef purple fill:#ffe1f5,stroke:#d946ef,stroke-width:2px,color:#000;

        class Attacker red;
        class Agents,Tools yellow;
        class Tasks purple;

        style dashed_box stroke-dasharray: 5 5, fill:none,stroke:#333,stroke-width:2px;
    ```

<br />

-   **Model Context Protocol (MCP)**

    Attackers may exploit MCP to manipulate tool discovery and the agent’s behavior when interacting with tools.

    **Examples of tools:** web search, web fetch, code execution, email, file system.

    ``` mermaid
    graph LR

        subgraph dashed_box_genai ["GenAI System"]
            Agents["<span style='color:#000'>Agents</span>"]
        end

        subgraph dashed_box_mcp ["MCP Server"]
            Tools["<span style='color:#000'>Tools</span>"]
            Client["<span style='color:#000'>MCP Client</span>"]
        end

        Agents -->|"Discovery"| Client
        Client --> Tools

        Attacker(["<span style='color:#000'>Attacker</span>"]) -.->|"Malicious Context<br />Malicious Instructions"| Tools

        Tools -->|"Execute"| Tasks["<span style='color:#000'>Tasks</span>"]

        classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
        classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
        classDef blue fill:#e0e7ff,stroke:#5f6de9,stroke-width:2px,color:#000;
        classDef purple fill:#ffe1f5,stroke:#d946ef,stroke-width:2px,color:#000;

        class Attacker red;
        class Agents yellow;
        class Client,Tools blue;
        class Tasks purple;

        style dashed_box_genai stroke-dasharray: 5 5, fill:none,stroke:#333,stroke-width:2px;
        style dashed_box_mcp stroke-dasharray: 5 5, fill:none,stroke:#333,stroke-width:2px;
    ```

<br />

-   **Agent2Agent Protocol (A2A)**

    Attackers may exploit A2A to manipulate agent’s discovery and collaboration, by poisoning Agents Cards `JSON` fields, or by exploiting task management.

    **Examples of A2A Agend Card fields:** name, description, skills, skills/id, skills/name, skills/description, skills/examples.

    ``` mermaid
    graph LR

        subgraph dashed_box_genai ["GenAI System"]
            SourceAgent["<span style='color:#000'>Source Agent</span>"]
        end

        subgraph dashed_box_a2a ["A2A Server"]
            Client["<span style='color:#000'>A2A Client</span>"]
            Card["<span style='color:#000'>Agents Cards</span>"]
        end

        SourceAgent -->|"Discovery"| Client
        Client --> Card

        Attacker(["<span style='color:#000'>Attacker</span>"]) -.->|"Malicious Context<br />Malicious Instructions"| Card

        Card -->|"Interacts"| TargetAgents["<span style='color:#000'>Target Agents</span>"]

        classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
        classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
        classDef blue fill:#e0e7ff,stroke:#5f6de9,stroke-width:2px,color:#000;
        classDef purple fill:#ffe1f5,stroke:#d946ef,stroke-width:2px,color:#000;

        class Attacker red;
        class SourceAgent yellow;
        class Client,Card blue;
        class TargetAgents purple;

        style dashed_box_genai stroke-dasharray: 5 5, fill:none,stroke:#333,stroke-width:2px;
        style dashed_box_a2a stroke-dasharray: 5 5, fill:none,stroke:#333,stroke-width:2px;
    ```

    ``` mermaid
    graph LR

        subgraph dashed_box_genai ["GenAI System"]
            SourceAgent["<span style='color:#000'>Source Agent</span>"]
        end

        subgraph dashed_box_a2a ["A2A Server"]
            Client["<span style='color:#000'>A2A Client</span>"]
            TaskMng["<span style='color:#000'>Task Manager</span>"]
        end

        SourceAgent -->|"Discovery"| Client
        Client --> TaskMng

        Attacker(["<span style='color:#000'>Attacker</span>"]) -.->|"Malicious Tasks"| TaskMng

        TaskMng -->|"Interacts"| TargetAgents["<span style='color:#000'>Target Agents</span>"]

        classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
        classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
        classDef blue fill:#e0e7ff,stroke:#5f6de9,stroke-width:2px,color:#000;
        classDef purple fill:#ffe1f5,stroke:#d946ef,stroke-width:2px,color:#000;

        class Attacker red;
        class SourceAgent yellow;
        class Client,TaskMng blue;
        class TargetAgents purple;

        style dashed_box_genai stroke-dasharray: 5 5, fill:none,stroke:#333,stroke-width:2px;
        style dashed_box_a2a stroke-dasharray: 5 5, fill:none,stroke:#333,stroke-width:2px;
    ```

<br />

-   **Infrastructure Events**

    Attackers may trigger GenAI processing pipelines via backend events.

    **Examples of events:** File upload triggers (initiating embedding generation), Message Queue injection (forcing the model to process a malicious payload).

    ``` mermaid
    graph LR
        Attacker(["<span style='color:#000'>Attacker</span>"]) -->|"Trigger Event"| Queue["<span style='color:#000'>Message Queue/Bucket</span>"]
        Queue -->|"Auto-Process"| Pipeline["<span style='color:#000'>GenAI Pipeline</span>"]

        classDef red fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000;
        classDef yellow fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000;
        classDef purple fill:#ffe1f5,stroke:#d946ef,stroke-width:2px,color:#000;

        class Attacker red;
        class Queue purple;
        class Pipeline yellow;
    ```
