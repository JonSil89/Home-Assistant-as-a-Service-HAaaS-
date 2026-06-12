# Docs overview

Tämä hakemisto sisältää Home Stack / HAaaS -projektin tärkeimmät arkkitehtuuri-, roadmap-, requirements-, evidence- ja runbook-dokumentit.

## Mitä mistäkin löytyy

- `deployment_azure.md`
  - Mermaid-sekvenssikaavio Azure-deploy-pipeline’sta:
    - Git push → GitHub Actions
    - Azure Key Vault -tyyppinen salaisuuksien hallinta tuotantomallissa
    - Docker-imagen build + push Azure Container Registryyn (ACR)
    - Deploy Azure Container App / Web App -palveluun
- `database_schema.md`
  - HA:n `STATES`/`EVENTS`/`STATISTICS`-taulut + HAaaS-hallintataso (`USER_PROFILES`, `INSTANCES`).
  - Hyvä referenssi, kun mietit mitä dataa tallennetaan ja mihin kerrokseen.
- `development_guide.md`
  - Home Assistantin YAML-syntaksin ja konfiguroinnin perusopas.
  - Käytä tätä, kun lisäät esimerkkejä HA-konfiguraatiosta tai selität, miten IaC tuottaa HA:n konffit.
- `dlcm_lifecycle.md`
  - Kuvaa Digital Lifecycle Management -mallin vaiheineen (Day 0 → Day N → decommission).
- `requirements.md`
  - Ei-koodilliset vaatimukset: operointi, turvallisuus, dokumentointi, lifecycle ja tulevat tekniset vaatimukset.
- `roadmap_llm.md`
  - LLM/Assist-kerroksen arkkitehtuuri (UI → LLM → työkalut → HA API → fyysiset entiteetit).
  - Lähtökohta, jos toteutat agentteja tai tekoälyavusteista automaatiota.
- `roadmap_pinecone.md`
  - RAG- / vektorihakuroadmap: Markdown-dokumenttien ingestointi → embeddingit → vektoritietokanta (FAISS/Pinecone) → LLM-kyselyt.
- `evidence/VALIDATION_REPORT_EXAMPLE.md`
  - Stabiili esimerkki validointiraportista portfolio- ja audit-evidence-käyttöön.
- `runbooks/LOCAL_VALIDATION.md`
  - Ohje paikalliseen validointiin ennen muutosten puskemista.

## Suositeltu lukujärjestys

1. Lue ensin juuren `README.MD` nykytilan ja rajauksen ymmärtämiseksi.
2. Lue `database_schema.md`, `dlcm_lifecycle.md` ja `requirements.md` kokonaiskuvaa varten.
3. Lue `deployment_azure.md` kun mietit CI/CD:tä ja Azure-topologiaa.
4. Lue `roadmap_llm.md` ja `roadmap_pinecone.md`, jos työskentelet LLM- ja RAG-kerrosten parissa.
5. Käytä `development_guide.md` -tiedostoa referenssinä aina, kun kirjoitat HA:n YAML-konfiguraatioita.
6. Aja lopuksi validointi `runbooks/LOCAL_VALIDATION.md` -ohjeen mukaan.
