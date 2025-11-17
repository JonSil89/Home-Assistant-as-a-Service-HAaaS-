Readme.md 

graph TD
    subgraph KÄYTTÖLIITTYMÄ / SYÖTE["A: Käyttäjä / UI-syöte (Esimerkki Payloads)"]
        A_FE[Frontend/Mobile App: POST /api/tools/light_control]
        A_VA[Voice Assistant: Intent Mapping -> POST /api/tools/climate_control]
        A_AS[Automation Scheduler: POST /api/tools/scene]
        A_TP[Third-party: POST /api/custom/bridge]
        A_ASSIST[Assist API: POST /api/assist (Prompt + Tools Metadata)]
    end

    subgraph LLM["🤖 Large Language Model (B, C, D)"]
        B["B: LLM vastaanottaa (Prompt + Tools + Konteksti)"]
        C["C: Päätöksenteko (Työkalun valinta, parametrit, turvatarkistukset)"]
        D["D: Suorita työkalukutsu (Formatoidaan API-pyynnöksi)"]
    end

    subgraph HA_API["E: Home Assistant Assist/Custom API"]
        E_EP[HTTP/WebSocket-rajapinta]
    end

    subgraph TYÖKALUT["F: Toiminnalliset Työkalut / Endpointit"]
        F_T[TimeTool (GET /api/tools/time)]
        F_L[LightControl (POST /api/tools/light_control)]
        F_C[ClimateControl (POST /api/tools/climate_control)]
        F_N[NotificationTool (POST /api/tools/notify)]
        F_S[SceneTool (POST /api/tools/scene)]
    end

    subgraph ENTITEETIT["G: Entiteetit, Tilat, Palvelut"]
        G_E[Entities: light.kitchen, climate.living_room]
    end

    A_FE --> E_EP
    A_VA --> E_EP
    A_AS --> E_EP
    A_TP --> E_EP
    A_ASSIST --> B
    
    B --> C
    C --> D
    D --> E_EP
    
    E_EP --> F_T
    E_EP --> F_L
    E_EP --> F_C
    E_EP --> F_N
    E_EP --> F_S
    
    F_L --> G_E
    F_C --> G_E
    
    G_E --> F_L[Tilan päivitys takaisin työkaluun]
    F_S --> G_E[Tilan päivitys takaisin työkaluun]
    
    F_T --> D[Työkalun vastaus]
    F_L --> D
    F_C --> D
    F_N --> D
    F_S --> D
    
    D --> B[LLM saa vastauksen ja jatkaa keskustelua]
