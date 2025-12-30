# Digital Lifecycle Management (DLCM) – elinkaari

Tämä dokumentti kuvaa, miten yksi hallittu Home Assistant -instanssi elää koko elinkaarensa HAaaS-mallissa.

## 1. Provisioning (Day 0)

Tavoite: luoda toistettava, koodilla hallittu perusinfrastruktuuri.

- Työkalut: Terraform / Ansible / PowerShell DSC.
- Tyypilliset vaiheet:
  - Azure-resurssien luonti (resource group, verkot, tallennus, Container Apps / Web App, ACR).
  - Perus-OS / container host -konfiguraatio.
  - Turvaperusta: palomuurit, identiteetti (Azure AD), lokitus.

Tuloksena on "tyhjä" mutta valmis ympäristö, johon HA voidaan ajaa.

## 2. Onboarding (Day 1)

Tavoite: saada konkreettinen HA-instanssi käyttöön hallitulla tavalla.

- Home Assistant Core käynnistetään provisionoidussa ympäristössä (Docker / Azure Container Apps).
- Konfiguraatio tuodaan Gitistä / IaC:stä:
  - integraatiot, automaatiot, salaisuudet (Key Vault / secrets), käyttäjät.
- HAaaS-hallintatasolla päivitetään:
  - `USER_PROFILES` (omistaja / tenant),
  - `INSTANCES` (region, status, viimeinen backup, yms. – ks. `database_schema.md`).

Tuloksena instanssi, joka näkyy hallintapaneelissa sekä teknisesti että liiketoiminnallisesti.

## 3. Operate & Observe (Day N)

Tavoite: pitää instanssi terveenä, turvallisena ja läpinäkyvänä.

- HA:n telemetria:
  - `STATES` / `EVENTS` / `STATISTICS` taulut keräävät tilat, tapahtumat ja aggregaatit.
- Valvonta ja mittarointi:
  - Prometheus + Grafana (tai vastaavat) keräävät metrikat HA:sta ja tausta-alustasta.
  - Dashboardit näyttävät sekä teknisen tilan (CPU, muistinkäyttö, viiveet) että liiketoimintatason mittarit (aktiiviset instanssit, virheelliset automaatiot, jne.).
- Varautuminen:
  - säännölliset backupit (tiedot `INSTANCES.last_backup`),
  - testatut palautusprosessit.

## 4. Päivitykset ja rollback (DLCM ydin)

Tavoite: pystyä päivittämään Home Assistant -palvelu ja siihen liittyvät komponentit turvallisesti.

- Build-vaihe:
  - Git push → CI (GitHub Actions / GitLab CI) → Docker image → Azure Container Registry.
- Julkaisu:
  - Uusi versio rullataan ensin rajatulle joukolle instansseja (canary/pilotit).
  - Onnistumisen jälkeen laajennetaan muihin instansseihin.
- Rollback:
  - jos metrikat / lokit / asiakkaiden palaute osoittaa ongelmia,
  - instanssit osoitetaan nopeasti edelliseen image-versioon.

Kaikki tämä tulisi mallintaa pipelineina (`deployment_azure.md` visualisoi high level -kulun).

## 5. Decommission (EOL)

Tavoite: lopettaa instanssi hallitusti ja auditointikelpoisesti.

- Ennen poistoa:
  - otetaan viimeinen backup,
  - tarvittaessa anonymisoidaan / poistetaan henkilötiedot (GDPR).
- IaC poistaa Azure-resurssit kontrolloidusti.
- `INSTANCES`-taulu päivitetään esim. tilaan `decommissioned`, ja mahdollinen linkki `USER_PROFILES`-tietoihin säilyttää auditjäljen.

## 6. Suhde muihin dokumentteihin

- `README.MD` kuvaa korkean tason liikeidean, segmentit ja arvolupauksen.
- `database_schema.md` tarkentaa, mitä tietoa HA-telemetriakerros ja HAaaS-hallintakerros tallettavat.
- `deployment_azure.md` näyttää CI/CD-kulun yhdelle julkaisu-/päivityssyklille.

Kun suunnittelet uutta ominaisuutta tai prosessia, varmista että se sopii johonkin näistä DLCM-vaiheista eikä riko niiden selkeyttä.