<!-- [START BADGES] -->
[![CI](https://github.com/JonSil89/Home-Assistant-as-a-Service-HAaaS-/actions/workflows/blank.yml/badge.svg)](https://github.com/JonSil89/Home-Assistant-as-a-Service-HAaaS-/actions/workflows/blank.yml)
<!-- [END BADGES] -->

## Yleiskuvaus

**Home Assistant as a Service (HAaaS)** on suomalainen IoT-projektialusta, joka yhdistää **Home Assistantin avoimen lähdekoodin joustavuuden** ja **yritystason hallittavuuden**.  
Tavoitteena on rakentaa palvelu, joka mahdollistaa automaation ja älykotien hallinnan helposti, turvallisesti ja ammattimaisesti – ilman DIY-asennuksen monimutkaisuutta.

Projektin keskiössä on **Infrastructure as Code (IaC)** ja **Digital Lifecycle Management (DLCM)** -malli, joka tekee Home Assistant -ratkaisuista skaalautuvia, hallittavia ja luotettavia.

> “Avoin kuin Home Assistant. Luotettava kuin kaupallinen järjestelmä.”

---

## Missio

Luoda hallittu, avoimeen lähdekoodiin perustuva automaatioekosysteemi, joka yhdistää modernin IT-palvelutuotannon, automaation ja pilviarkkitehtuurin parhaat puolet.  
Tavoitteena on tehdä Home Assistantista palvelu, jota voi käyttää kuka tahansa – ilman asennus- tai ylläpitohaasteita.

---

## Keskeinen idea

| Osa-alue | Kuvaus |
|-----------|--------|
| **Core Platform** | Home Assistant (Open Source) |
| **IaC Layer** | Automatisoidut asennukset ja konfiguraatiot (Ansible, Terraform, PowerShell DSC) |
| **DLCM Layer** | GitLab CI/CD, testaus- ja julkaisuputket |
| **Hosting** | Azure / Docker / paikallinen laite (Raspberry Pi, NUC) |
| **Monitoring** | Prometheus, Grafana, Home Assistant Supervisor |
| **Documentation** | GitBook + AI-avusteinen dokumentaatio |
| **Business Model** | Subscription-pohjainen hallintapalvelu (Home Assistant as a Service) |

---

## Markkinanäkymä

Nykyinen markkina on jakautunut kahteen ääripäähän:

| Segmentti | Vahvuudet | Puutteet |
|------------|------------|-----------|
| **DIY (Home Assistant, OpenHAB)** | Vapaa, avoin, joustava | Vaatii teknistä osaamista, ei tukea, ei skaalaudu |
| **Kaupalliset (Google Home, Apple HomeKit, Verisure)** | Helppokäyttöinen, luotettava | Suljettu ekosysteemi, korkea hinta, ei räätälöitävissä |

**HAaaS sijoittuu näiden väliin:**  
Yhdistämme kaupallisten palvelujen helppokäyttöisyyden ja DIY-järjestelmien avoimuuden.

---

## Arvolupaus

- Helppo käyttöönotto ja automaattiset päivitykset  
- Täysi avoimen lähdekoodin joustavuus ja räätälöitävyys  
- Ammattimainen ylläpito ja tukipalvelu  
- Turvallinen ja GDPR-yhteensopiva arkkitehtuuri  
- Skaalautuva malli yksittäisistä kotitalouksista suuriin kiinteistöverkostoihin

---

## Kohderyhmät

| Kohderyhmä | Tarve | Ratkaisu |
|-------------|--------|-----------|
| **Kiinteistönomistajat / Isännöitsijät** | Kiinteistöjen energian ja olosuhteiden seuranta | Keskitetty, automatisoitu hallintapaneeli ilman IT-osastoa |
| **PK-yritykset** | Räätälöidyt automaatioratkaisut (valaistus, kulunvalvonta, tilavaraukset) | “Me hoidamme IT:n, te keskitytte liiketoimintaan.” |
| **Teknologisesti suuntautuneet kuluttajat** | Home Assistant ilman teknistä säätöä | Kaikki ominaisuudet, nolla asennusstressiä |

---

## Tekninen fokus

- **Infrastructure as Code (IaC)** – vakioidut ja toistettavat ympäristöt  
- **Digital Lifecycle Management (DLCM)** – automaattinen päivitys-, testaus- ja rollback-prosessi  
- **Pilvi- ja paikallinen hosting** – Azure, Docker, Raspberry Pi  
- **Tietoturva ja Compliance** – GDPR, ISO 27001, NIST-periaatteet  
- **Monitoring & Telemetria** – Grafana, Prometheus, HA Supervisor  
- **CI/CD Pipeline** – GitLab Runners, versionhallinta ja julkaisut automaattisesti  

---

## MVP (Minimum Viable Product)

| Vaihe | Tavoite | Työkalut |
|--------|----------|-----------|
| **1. Proof of Concept** | Yksi hallittu Home Assistant -instanssi IaC:n kautta | Ansible, Docker |
| **2. Pilotointi** | Ensimmäiset testiasiakkaat (kuluttaja / pk-yritys) | Azure-hosted HA |
| **3. DLCM-testaus** | Automaattiset päivitykset ja valvonta | GitLab CI/CD |
| **4. Tilausmalli** | Subscription-palvelun julkaisu | Stripe, Web-portal |

---

## Hinnoitteluluonnos

| Paketti | Kuvaus | Hinta / kk |
|----------|---------|------------|
| **Starter** | Peruskäyttö kotiin (5 automaatiota) | 9,90 € |
| **Pro** | Laajempi automaatio ja etähallinta | 29,90 € |
| **Business** | Räätälöity yritysympäristö | 99,00 €+ |
| **Enterprise** | Taloyhtiöt ja kiinteistöverkostot | Pyynnöstä |

---

## Tietoturva ja sääntely

- GDPR-yhteensopiva arkkitehtuuri  
- IAM ja käyttövaltuushallinta (Azure AD, paikallinen HA)  
- ISO 27001 / NIST -vaatimustenmukainen dokumentointi  
- Turvallinen päivitysketju CI/CD:n kautta  
- Säännölliset auditointitestit ja lokienhallinta  

---

## Etenemispolku

1. **MVP:n viimeistely** (Home Assistant + IaC)  
2. **Pilottiasiakkaiden testaus** (B2C ja B2B)  
3. **DLCM-järjestelmän integrointi ja dokumentaatio**  
4. **Brändi ja verkkosivusto**  
5. **Sijoittaja- ja kumppaniverkoston rakentaminen**

---

## Teknologiat ja työkalut

- **IaC / Automaatio:** Ansible, Terraform, PowerShell DSC  
- **CI/CD ja DevOps:** GitLab, Docker, Azure Pipelines  
- **Dokumentointi:** GitBook, Markdown, AI-assistant (OpenAI)  
- **Valvonta:** Grafana, Prometheus  
- **Hosting:** Azure, paikallinen laitteisto  
- **Tietoturva:** Defender, IAM, GPO, GDPR Compliance

---

## Yhteistyö ja jatkokehitys

Projektin pitkän aikavälin tavoitteena on muodostaa **modulaarinen IoT-ekosysteemi**, johon voidaan liittää uusia integraatioita ja kaupallisia laajennuksia.  
Tämä sisältää mm.:

- Laitekohtaiset moduutit (esim. Shelly, Zigbee, Z-Wave)  
- Pilvipohjaiset API-integraatiot (Azure IoT Hub, MQTT)  
- AI-avusteinen automaation hallinta  
- Smart Energy -ominaisuudet ja analytiikka  

---

## Tietoa tekijästä

**Jonne Silvennoinen**  
IT-asiantuntija & tekninen dokumentoija  
Erikoistunut Microsoft 365-, Azure-, IaC- ja automaatioympäristöihin.  
Kokemusta moniasiakas- ja hyvinvointialueympäristöistä, joissa tietoturva ja dokumentaatio ovat keskiössä.  
Kiinnostunut avoimen lähdekoodin ratkaisuista, IoT:sta ja modernista IT-palvelutuotannosta.

📧 **jonne.silvennoinen89@gmail.com**  
🌐 [LinkedIn](https://www.linkedin.com/in/jonne-silvennoinen-0421aa266/)  
💾 [GitHub](https://github.com/jonnesilvennoinen)

---

## Lisenssi

Tämä projekti on **open source**, mutta sen kaupallinen laajennus (HAaaS Managed Service) on erillisen lisenssisopimuksen alainen.  
Lisätiedot ja kaupalliset yhteistyöt: ota yhteyttä sähköpostitse.

---
