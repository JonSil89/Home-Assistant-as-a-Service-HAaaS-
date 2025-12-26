

    subgraph Embedding_Process
        B -->|Chunking| C{OpenAI Embedding Model}
        C -->|Vectorize| D[High-Dimensional Vectors]
    end

    subgraph Vector_Database
        D -->|Upsert| E[(Pinecone Index)]
    end

    subgraph AI_Query_Flow
        F[User Question] -->|Context Search| E
        E -->|Relevant Context| G[LLM / AI Agent]
        G -->|Accurate Answer| H[Final Response]
    end

    style E fill:#00c853,stroke:#333,stroke-width:2px
    style G fill:#2979ff,stroke:#333,stroke-width:2px
