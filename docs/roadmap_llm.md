```Mermaid


graph TD
    %% UI Layer - User Interface & Inputs
    subgraph UI_LAYER ["A: User Interface & Inputs"]
        A_FE[Frontend/Mobile App]
        A_VA[Voice Assistant]
        A_AS[Automation Scheduler]
        A_ASSIST[Assist API - Prompt + Tools]
    end

    %% AI Engine - Decision Logic
    subgraph LLM_CORE ["🤖 AI Engine (Decision Logic)"]
        B["B: Receive Context & Tools"]
        C["C: Decision Making & Safety Checks"]
        D["D: Execute Tool Call"]
    end

    %% Home Assistant API Layer
    subgraph HA_API ["E: Home Assistant API Layer"]
        E_EP[HTTP/WebSocket Interface]
    end

    %% Functional Tools / Endpoints
    subgraph TOOLS ["F: Functional Tools / Endpoints"]
        F_T[TimeTool]
        F_L[LightControl]
        F_C[ClimateControl]
        F_N[NotificationTool]
    end

    %% Physical Infrastructure
    subgraph ENTITIES ["G: Physical Infrastructure"]
        G_E[Entities: Lights, Climate, Sensors]
    end

    %% Flow logic - Connecting the components
    A_FE & A_VA & A_AS --> E_EP
    A_ASSIST --> B
    B --> C
    C --> D
    D --> E_EP
    E_EP --> F_T & F_L & F_C & F_N
    F_L & F_C --> G_E
    G_E -.->|State Update| D
    D -.->|LLM Response| 

  
```
