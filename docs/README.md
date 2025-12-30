# Docs overview

Tämä hakemisto sisältää Home Stack / HAaaS -projektin tärkeimmät arkkitehtuuri- ja roadmap-dokumentit.

## Mitä mistäkin löytyy

- `deployment_azure.md`
  - Mermaid-sekvenssikaavio Azure-deploy-pipeline’sta:
    - Git push → GitHub Actions
    - Salaisuudet Azure Key Vaultista
    - Docker-imagen build + push Azure Container Registryyn (ACR)
    - Deploy Azure Container App / Web App -palveluun
- `database_schema.md`
  - HA:n `STATES`/`EVENTS`/`STATISTICS`-taulut + HAaaS-hallintataso (`USER_PROFILES`, `INSTANCES`).
  - Hyvä referenssi, kun mietit mitä dataa tallennetaan ja mihin kerrokseen.
- `development_guide.md`
  - Home Assistantin YAML-syntaksin ja konfiguroinnin perusopas.
  - Käytä tätä, kun lisäät esimerkkejä HA-konfiguraatiosta tai selität, miten IaC tuottaa HA:n konffit.
- `roadmap_llm.md`
  - LLM/Assist-kerroksen arkkitehtuuri (UI → LLM → työkalut → HA API → fyysiset entiteetit).
  - Lähtökohta, jos toteutat agentteja tai tekoälyavusteista automaatiota.
- `roadmap_pinecone.md`
  - RAG- / vektorihakuroadmap: Markdown-dokumenttien ingestointi → embeddingit → vektoritietokanta (FAISS/Pinecone) → LLM-kyselyt.
- `requirements.txt/`
  - Tällä hetkellä vain `pinecone-client`-placeholder, joka kertoo, että tähän on tarkoitus kerätä tarkempia vaatimuksia liittyen vektorihakukerrokseen.
- `dlcm_lifecycle.md`
  - (Uusi) kuvaa koko Digital Lifecycle Management -mallin vaiheineen (Day 0 → Day N → decommission).

## Suositeltu lukujärjestys

1. Lue ensin juuren `README.MD` (liiketoiminta + high level -arkkitehtuuri).
2. Sen jälkeen:
   - `database_schema.md` ja `dlcm_lifecycle.md` kokonaiskuvaa varten.
   - `deployment_azure.md` kun mietit CI/CD:tä ja Azure-topologiaa.
   - `roadmap_llm.md` ja `roadmap_pinecone.md` jos työskentelet LLM- ja RAG-kerrosten parissa.
3. Käytä `development_guide.md` -tiedostoa referenssinä aina, kun kirjoitat HA:n YAML-konfiguraatioita.