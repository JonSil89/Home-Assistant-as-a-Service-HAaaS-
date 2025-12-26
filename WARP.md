# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository overview

This repository defines **Home Stack / Home Assistant as a Service (HAaaS)** – a managed Home Assistant offering combining open-source Home Assistant flexibility with infrastructure-as-code (IaC), Digital Lifecycle Management (DLCM), and strong compliance/documentation practices.

The current main branch is primarily **architectural and conceptual**:
- `README.MD` describes mission, positioning between DIY and commercial smart home platforms, DLCM focus, and high-level technical stack (Ansible/Terraform, Docker/Azure Container Apps, GitLab CI/CD, Prometheus/Grafana, Cloudflare Tunnel, Azure, security/compliance).
- `docs/` contains Mermaid diagrams and narrative docs for configuration conventions, Azure deployment flow, data model, LLM integration, vector search, and requirements.
- There is **no application source code or test suite yet**; the repo is an architecture and requirements sandbox.

Note: Some of the files referenced below may have been deleted or moved in later commits. If they are missing in your working tree, you can still inspect them from history using e.g. `git --no-pager show <commit>:<path>`.

## Important documentation

These documents are the main sources of truth for understanding the system. Prefer reading them before making significant changes.

- **High-level product and architecture** – `README.MD`
  - Project name: *Home Stack – Automated Infrastructure & Data Quality*.
  - Describes positioning between DIY Home Assistant and commercial services, target customer segments, pricing sketches, and long-term vision.
  - Summarizes technical focus areas: IaC, DLCM, Azure/cloud + local hosting, monitoring (Grafana/Prometheus), CI/CD (GitLab, pipelines), and security/compliance (GDPR, ISO 27001, NIST principles).

- **Home Assistant configuration concepts** – `docs/development_guide.md`
  - High-level intro to Home Assistant YAML:
    - Integrations vs platforms, mappings (`key: value`) and lists (`- item`).
    - Indentation rules (spaces only, typically 2 spaces per level).
    - Environment-variable based configuration via `!env_var` and split configuration via `!include`.
  - Use this as conceptual guidance when adding configuration snippets or discussing how configuration could be structured; it is not a full development guide for this specific repo.

- **Azure deployment flow** – `docs/deployment_azure.md`
  - Sequence diagram for the intended CI/CD pipeline:
    - Developer pushes to `main`.
    - GitHub Actions runs build/test jobs.
    - Secrets are fetched from **Azure Key Vault** (e.g., API keys, DB creds).
    - Docker image is built and pushed to **Azure Container Registry (ACR)**.
    - **Azure Container Apps / Web App** pulls the image and starts the service.
    - Deployment reports success and provides an accessible URL.
  - When implementing actual CI/CD, align workflow steps with this diagram (Key Vault for secrets, ACR for images, ACA for runtime).

- **Data model & management plane** – `docs/database_schema.md`
  - Mermaid ER diagram describing two main layers:
    - **Home Assistant core data**: `STATES`, `STATE_ATTRIBUTES`, `EVENTS`, `STATISTICS`, `STATISTICS_SHORT_TERM`.
    - **HAaaS management layer**: `USER_PROFILES` (user id, email, subscription plan) and `INSTANCES` (managed HA instance metadata: region, status, last backup, etc.).
  - When designing new features, keep the separation between **per-instance HA telemetry** and **service-level management metadata**.

- **AI / LLM Assist roadmap** – `docs/roadmap_llm.md`
  - Conceptual architecture for an "Assist" layer:
    - **UI layer**: frontend/mobile app, voice assistant, automation scheduler, Assist API.
    - **LLM core**: receives context & tools, performs decision-making + safety checks, executes tool calls.
    - **Home Assistant API layer**: HTTP/WebSocket interface.
    - **Tools/endpoints**: e.g. `TimeTool`, `LightControl`, `ClimateControl`, `NotificationTool`.
    - **Physical entities**: lights, climate devices, sensors; state changes feed back into the LLM loop.
  - This is a **design roadmap**, not implemented code. If you add LLM-based automation, align tool boundaries and safety/feedback loops with this model.

- **Vector search / Pinecone roadmap** – `docs/roadmap_pinecone.md`
  - Describes an ingestion pipeline where markdown docs (`docs/*.md`, `README.MD`) are:
    - Read by a Python script.
    - Chunked and embedded via an OpenAI embedding model.
    - Upserted into a vector database (e.g. **Pinecone index**).
  - Queries are answered by retrieving relevant context from the index and passing it to an LLM.
  - Combine this with the environment design in `.env.example` when you eventually implement ingestion.

- **Requirements and constraints** – `requirements.txt`
  - Not a Python dependency file; instead, a placeholder for:
    - Compliance mappings (GDPR, ISO 27001, etc.).
    - Operational requirements (SLOs, availability, backup policies).
    - Architecture constraints and design decisions.
    - Security and lifecycle requirements.
  - Extend this document as you formalize non-functional requirements.

- **Environment template** – `.env.example`
  - Defines required environment variables for future implementation (placeholders only):
    - Application settings: `APP_ENV`, `APP_NAME`, `LOG_LEVEL`, `ALLOW_DEBUG`, directory paths.
    - Vector DB: `VECTOR_DB_TYPE` (`faiss` | `pinecone` | other), `VECTOR_DB_PATH`.
    - Pinecone config: API key, environment, index name.
    - Embeddings / AI: provider (`openai` | `local` | `azure`), embedding model name, OpenAI API key.
    - Data ingestion: ClickUp API token and team id.
    - Compliance flags: `COMPLIANCE_STANDARD`, `VALIDATION_STRICT_MODE`.
  - Use this file as the canonical list of env-vars. Actual secret values must come from secure stores (Key Vault, local `.env` excluded from VCS, GitHub/Azure secrets), not committed files.

## Commands and workflows

There is **no concrete application build, lint, or test pipeline implemented yet**. Most automation is still conceptual. The only concrete, repo-specific commands defined so far are:

- **Initialize local environment file**
  - Based on `main.yml` task:
    - On Unix-like shells: `cp .env.example .env`
    - On PowerShell: `Copy-Item .env.example .env`
  - Then edit `.env` with real values (kept out of version control).

- **Inspect historical documentation if missing locally**
  - If you see that docs/README are missing but you know they existed:
    - List files in the last commit: `git --no-pager ls-tree -r --name-only HEAD`
    - Show a specific historical file: `git --no-pager show HEAD:docs/deployment_azure.md`
  - This is useful if the working tree has staged deletions but you still want to reference older diagrams.

- **Warp workflow for theme preview generation (not core to HAaaS)**
  - The repo includes a Warp workflow definition under `.github/workflows/.warp/workflows/.warp/workflows/run_themes_generator.yml`:
    - It declares a command: `python3 ./scripts/gen_theme_previews.py {{directory}}`.
    - The referenced `scripts/gen_theme_previews.py` script is **not present** in this repo; treat this workflow as an example/snippet rather than a maintained part of this project.

At this stage there is **no test framework or application entrypoint** wired up, so there is no canonical way to "run a single test" or start the application. Future contributors should:
- Introduce language/runtime-specific tooling (e.g., Python `pytest`, Node `npm test`, Terraform `terraform validate`, etc.).
- Document concrete commands in `README.MD` and/or update this `WARP.md` once implementation exists.

## High-level architecture

### 1. Azure + Home Assistant topology (DLCM view)

From `README.MD` and the architecture Mermaid diagrams, the "happy path" for one managed Home Assistant instance looks like this:

- **Provisioning (Day 0)**
  - Terraform/Ansible (and optionally PowerShell DSC) create Azure resources and base OS/container configuration.
  - Target runtimes are **Docker** and **Azure Container Apps / Web App**, fronted by Cloudflare Tunnel for secure remote access.

- **Configuration & onboarding (Day 1)**
  - Home Assistant Core is started in the provisioned environment.
  - Initial integrations, secrets, and HA configuration are applied (conceptually driven from Git + IaC, not yet implemented in code here).
  - Instance metadata (region, status, owner) is recorded in the HAaaS management layer (see section 2).

- **Operate & observe (Day N)**
  - Telemetry (states, events, statistics) is persisted in HA’s backing store (e.g. InfluxDB or MariaDB) per `docs/database_schema.md`.
  - Prometheus/Grafana (planned) scrape metrics and expose dashboards for both platform health and HAaaS service-level indicators.

- **Update & rollback (DLCM)**
  - Git-based CI/CD (GitHub Actions today, GitLab CI/CD mentioned in docs) builds and publishes container images to **Azure Container Registry (ACR)**.
  - Deployments to Azure Container Apps pull from ACR; the DLCM intent is:
    - Validate new versions (smoke tests / canary).
    - Roll out across instances in a controlled way.
    - Provide a clear rollback path by re-pointing instances to previous images.

- **Decommissioning (End of life)**
  - HA instance is drained (backups, data export, and last telemetry snapshots).
  - Azure resources are destroyed via IaC.
  - Management records (`INSTANCES`, potentially related `USER_PROFILES` links) are updated to reflect decommissioned state.

### 2. Service management plane (HAaaS)

The `docs/database_schema.md` diagram formalizes a **two-layer data model**:

- **Home Assistant telemetry**:
  - `STATES` + `STATE_ATTRIBUTES` represent entity states over time.
  - `EVENTS` capture triggers and event types.
  - `STATISTICS` and `STATISTICS_SHORT_TERM` support aggregations and short-term analytics.

- **HAaaS management layer**:
  - `USER_PROFILES` captures tenants/end users (id, email, subscription plan).
  - `INSTANCES` represents managed Home Assistant instances (region, status, backups).

Any future code should respect this boundary:
- Home Assistant internals remain decoupled from the management plane.
- The HAaaS layer orchestrates provisioning, updates, and customer-facing operations across many HA instances.

### 3. LLM / Assist integration

The LLM roadmap (`docs/roadmap_llm.md`) adds an **intelligent Assist layer** on top of the HA and management planes:

- **UI/input layer**: frontend or mobile app, voice assistant interfaces, automation scheduler, and an Assist API surface.
- **LLM engine**: receives context and tool definitions, performs decision-making and safety checks, and then issues tool calls.
- **Home Assistant API layer**: HTTP/WebSocket interface mediating between the LLM and Home Assistant.
- **Tool endpoints**: abstract operations (time retrieval, light/climate control, notifications) that translate LLM intents into concrete HA actions.
- **Physical entity layer**: real-world devices whose state changes are fed back to the LLM via state updates, closing the loop.

When implementing LLM-backed automation, keep the following high-level design in mind:
- Encapsulate device-specific behavior behind well-defined tools.
- Preserve a clear boundary between **decision logic (LLM)** and **device operations (tools + HA API)**.
- Make state feedback explicit so the LLM can reason over current conditions instead of assuming success.

### 4. Knowledge and vector search layer

The Pinecone roadmap (`docs/roadmap_pinecone.md`) and `.env.example` describe a future **knowledge layer**:

- Markdown documentation (`docs/*.md`, `README.MD`) is the primary knowledge source.
- A Python-based ingestion component will:
  - Read and chunk docs.
  - Generate embeddings (default provider `openai`, model `text-embedding-3-large`).
  - Store vectors in a configurable vector DB (`faiss` locally or `pinecone` as a managed service`).
- An LLM or agent queries the vector index to retrieve relevant context before answering user questions.

No ingestion code currently exists in the repo, but environment variables and diagrams already encode the intended behavior. Respect these when adding any RAG/semantic search implementation.

### 5. CI/CD skeleton

- `.github/workflows/blank.yml` is a standard GitHub Actions starter workflow named `CI`:
  - On `push` / `pull_request` to `main`, runs on `ubuntu-latest`.
  - Currently only checks out the repo and runs simple `echo` commands.
  - Should be evolved to match the **Azure deployment** sequence in `docs/deployment_azure.md` once you add real build/test/deploy steps.

- Additional workflow files referenced in the tree (e.g., `ci`, `release`, `security`, `proof-html`) are conceptually present but not fully fleshed out in the current commit; treat them as placeholders for future CI enhancements.

## How future Warp instances should approach changes

- Start by reviewing `README.MD` and the diagrams in `docs/` to understand **intent and architecture** before writing any code.
- Check whether real application code, infrastructure modules, or tests have been added since this `WARP.md` was written. If so, prefer commands and conventions documented alongside that code over the conceptual material here.
- When introducing new tooling (test frameworks, deployment scripts, IaC modules), update both `README.MD` and this `WARP.md` to keep future agents aligned with the actual implementation.
