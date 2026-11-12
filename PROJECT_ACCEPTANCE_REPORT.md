# AI HelpDesk – Projektin loppuraportti ja kokonaisarviointi

**Raportin päiväys:** 12.11.2026  
**Tarkastelun kohde:** kouluprojektin toiminnallinen kokonaisuus ja dokumentoitu hyväksyntä  

## 1. Projektin tavoite ja toteutunut laajuus

AI HelpDesk on React/TypeScript-, FastAPI- ja MySQL-pohjainen verkkosovellus, jossa käyttäjä voi hallita omaa profiiliaan ja tukipyyntöjään sekä keskustella paikallisesti ajettavan Ollama-tekoälyn kanssa. Keskustelut ja viestit tallennetaan tietokantaan. Sovellukseen kuuluu myös rajattu dokumenttihakuun perustuva RAG-toiminto, suomen- ja englanninkielinen käyttöliittymä sekä Docker Compose -kehitys- ja esittely-ympäristö.

Projektinhallinnan ja hyväksyntäpäivitysten mukaan toteuttaja on vahvistanut kaikkien käyttäjätarinoiden US-01–US-17 käytännön hyväksymisen 05.11.2026. Tämä on toteuttajan dokumentoima hyväksyntä, ei ulkopuolisen auditoijan tekemä riippumaton varmennus.

## 2. Keskeiset toteutetut ominaisuudet

- Käyttäjän rekisteröityminen, kirjautuminen, uloskirjautuminen ja profiilin hallinta.
- Omien tukipyyntöjen luominen, tarkastelu, priorisointi ja sulkeminen.
- AI-chat, tallennettu keskusteluhistoria ja epäonnistuneen AI-vastauksen uudelleenyritys.
- Tukipyynnön luominen keskustelusta vasta käyttäjän tarkistuksen ja vahvistuksen jälkeen (US-09).
- Etusivun omien tukipyyntöjen yhteenveto: kokonaismäärä sekä OPEN- ja CLOSED-määrät (US-14).
- Suomen- ja englanninkielinen käyttöliittymä.
- RAG-haku rajatusta Markdown/TXT-dokumenttikokoelmasta avainsanoilla; lähdetiedot näytetään löydösten yhteydessä.
- Docker Compose -käynnistys frontendille, backendille, MySQL:lle, Redisille ja Ollamalle sekä valitulle paikalliselle mallille.

## 3. Testaus ja hyväksynnän näyttö

Projektidokumentaatioon kirjattu 05.11.2026 tilanne:

- Toteuttaja vahvisti kaikkien käyttäjätarinoiden US-01–US-17 hyväksymiskriteerien käytännön hyväksynnän.
- Koko Docker Compose -kokonaisuus käynnistettiin tyhjillä MySQL- ja Ollama-volyymeilla.
- Rekisteröitymisen ja kahdeksan rinnakkaisen kirjautumisen integraatiotesti läpäisi paikallisessa Compose/MySQL-ympäristössä.
- README:n mukaan backendin 86 testistä 85 läpäisi ja yksi valinnainen MySQL-integraatiotesti ohitettiin normaalissa ajossa; erikseen ajettu integraatiotesti läpäisi.
- Frontendin lint, TypeScript-tarkistus ja tuotantobuild onnistuivat.

Testitulokset kuvaavat dokumentoitua testaushetkeä. Ne eivät takaa virheettömyyttä kaikissa laite-, käyttöjärjestelmä- tai verkkoympäristöissä. AI-mallin vastausten laatu ja RAG-haun kattavuus ovat rajallisia ja riippuvat mallista, kysymyksen muotoilusta sekä käytettävissä olevista dokumenteista.

## 4. Tietoturvan yhteenveto

### Toteutettu projektissa

- Palvelinpuolen istunnot MySQL:ssä; allekirjoitettu eväste, HttpOnly, SameSite=Lax ja konfiguroitava Secure.
- Salasanojen scrypt-tiivistys ja satunnaiset suolat.
- Kirjautumisen Redis-pohjainen käyttörajoitus.
- Backendin omistajuustarkistukset tukipyynnöille ja keskusteluille.
- CORS- ja luotetun Originin tarkistukset osassa tilaa muuttavista pyynnöistä.
- Docker Compose -ympäristössä tietokanta ja Redis eivät julkaise host-portteja; palveluiden portit on rajattu paikalliseen loopback-käyttöön.

### Tietoturvahaaraan lisätty, mutta vielä testaamatta

Erillisessä haarassa `security/hardening-demo` on lisätty keskitetty Origin-tarkistus istuntoevästeen sisältäville tilaa muuttaville API-pyynnöille, rekisteröinnin IP-kohtainen käyttörajoitus, globaali AI-generoinnin lukko, yksityisten API-vastausten `no-store`-välimuistiasetus ja perustason tietoturvaotsakkeet. Muutoksia ei ole vielä varmennettu ajamalla testejä todellisessa Compose/MySQL/Redis-ympäristössä, eikä niitä pidä merkitä tuotannossa testatuiksi ennen tätä.

### Puutteet ja riskit LAN/WAN-käytössä

- Todellista kahden laitteen LAN-käyttöä, reverse proxyn IP-välitystä ja HTTPS-käyttöönottoa ei ole varmennettu.
- Nykyinen Compose on kehitys-/demoympäristö, ei valmis tuotantoratkaisu.
- WAN-käyttö edellyttäisi tuotantofrontendia, HTTPS-reverse proxya, palomuuria, sisäisten palveluiden eristystä ja tuotantokäyttöönoton erillistä tietoturvakatsausta.
- Tuotantokonttien vähimmät käyttöoikeudet, riippuvuuksien ja kuvien lukitus, pyyntökokojen rajat, kattava CSP, tuotannon API-dokumentaation sulkeminen, lokien valvonta ja palautusharjoitukset vaativat lisätyötä.
- Täydellistä kahden käyttäjän IDOR-testimatriisia ja riippumatonta penetraatiotestausta ei ole osoitettu.
- AI:n vastaukset voivat olla virheellisiä; paikallinen malli ja RAG eivät takaa ongelman ratkeamista.

Yksityiskohtaiset kontrollit, LAN/WAN-vaatimukset ja varmennettavat asiat on kuvattu erillisissä suomen- ja englanninkielisissä tietoturvadokumenteissa.

## 5. Avoimet toimitus- ja ylläpitoasiat

- Kolmansien osapuolten lisensseistä on tehty alustava inventointi, mutta projektin oman lisenssin valinta ja mahdolliset jakelukohtaiset toimet ovat avoinna.
- Todellinen LAN-verkkotestaus on tehtävä siinä ympäristössä, jossa sovellusta aiotaan käyttää.
- WAN-julkaisu ei kuulu kouluprojektin hyväksyttyyn toimituslaajuuteen.
- Tietoturvahaara on testattava ja arvioitava erikseen ennen mahdollista yhdistämistä päähaaraan.

## 6. Kokonaisarvio

Projektin dokumentoidun hyväksyntätilanteen perusteella kouluprojektin sovittu toiminnallinen laajuus US-01–US-17 on toteuttajan mukaan hyväksytty. Sovellus sisältää keskeisen tukipyyntöprosessin, AI-keskustelun, dokumenttihakuun perustuvan RAG-toiminnon, kaksikielisen käyttöliittymän ja toistettavan Docker Compose -kehitys-/demoympäristön.

**Hyväksyntä koskee kouluprojektin sovittua toiminnallista laajuutta ja dokumentoitua paikallista testausympäristöä. Se ei tarkoita, että sovellus olisi valmis tuotantokäyttöön LAN- tai WAN-verkossa tai että se olisi riippumattomasti tietoturva-auditoitu.**


---

# AI HelpDesk – Project Acceptance Report and Overall Evaluation

**Report date:** 12 November 2026  
**Review scope:** Functional scope of the student project and documented acceptance  

## 1. Project objective and delivered scope

AI HelpDesk is a web application built with React/TypeScript, FastAPI, and MySQL. Users can manage their profile and support tickets and chat with a locally hosted Ollama model. Conversations and messages are stored in the database. The application also includes a limited document-retrieval-based RAG feature, a Finnish/English user interface, and a Docker Compose development and demonstration environment.

According to the project management and acceptance records, the developer confirmed practical acceptance of all user stories US-01–US-17 on 5 November 2026. This is acceptance documented by the developer, not independent verification by an external auditor.

## 2. Main implemented features

- User registration, login, logout, and profile management.
- Creation, viewing, prioritization, and closure of the user's own support tickets.
- AI chat, saved conversation history, and retry of a failed AI response.
- Creating a support ticket from a conversation only after the user has reviewed and confirmed it (US-09).
- Dashboard summary of the user's tickets: total, OPEN, and CLOSED counts (US-14).
- Finnish and English user interface.
- Keyword-based RAG retrieval from a limited collection of Markdown/TXT documents, with source information shown alongside retrieved results.
- Docker Compose environment for the frontend, backend, MySQL, Redis, Ollama, and the selected local model.

## 3. Testing and acceptance evidence

The project documentation records the following status as of 5 November 2026:

- The developer confirmed practical acceptance of the acceptance criteria for all user stories US-01–US-17.
- The full Docker Compose environment was started with empty MySQL and Ollama volumes.
- Registration and an integration test involving eight concurrent logins passed in the local Compose/MySQL environment.
- According to the README, 85 of 86 backend tests passed, while one optional MySQL integration test was skipped during the normal test run; the integration test passed when run separately.
- Frontend linting, TypeScript checks, and the production build completed successfully.

These results describe the documented test run at that time. They do not guarantee defect-free operation across all hardware, operating systems, or network environments. AI response quality and RAG retrieval coverage are limited and depend on the model, question wording, and available documents.

## 4. Security summary

### Implemented in the project

- Server-side sessions stored in MySQL; signed session cookie with HttpOnly, SameSite=Lax, and configurable Secure attributes.
- scrypt password hashing with random salts.
- Redis-based login rate limiting.
- Backend ownership checks for support tickets and conversations.
- CORS and trusted-Origin checks on some state-changing requests.
- In the Docker Compose environment, the database and Redis do not publish host ports; service ports are bound to local loopback interfaces.

### Added to the security branch but not yet tested

The separate `security/hardening-demo` branch adds centralized Origin checks for state-changing API requests carrying a session cookie, IP-based registration rate limiting, a global AI-generation lock, `no-store` caching policy for private API responses, and baseline security headers. These changes have not yet been verified by running tests in the actual Compose/MySQL/Redis environment. They must not be described as runtime-tested until that verification is complete.

### Gaps and risks for LAN/WAN deployment

- LAN access using two actual devices, reverse-proxy client-IP forwarding, and HTTPS deployment have not been verified.
- The current Compose configuration is for development and demonstration, not a production-ready deployment.
- WAN deployment would require a production frontend, HTTPS reverse proxy, firewall rules, isolation of internal services, and a separate production security review.
- Further work is needed on least-privilege production containers, pinned dependencies and images, request-size limits, a complete CSP, disabling production API documentation, log monitoring, and backup restoration exercises.
- A complete two-user IDOR test matrix and independent penetration testing have not been demonstrated.
- AI responses may be incorrect; the local model and RAG do not guarantee that a user's problem will be solved.

Detailed controls, LAN/WAN requirements, and items requiring verification are described in the separate Finnish and English security documents.

## 5. Outstanding delivery and maintenance items

- A preliminary third-party license inventory has been completed, but selection of the project's own license and any distribution-related actions remain open.
- LAN network testing must be performed in the actual environment where the application is intended to run.
- WAN publication is outside the accepted scope of the student project.
- The security branch must be tested and reviewed separately before it is considered for merging into the main branch.

## 6. Overall evaluation

Based on the documented acceptance status, the developer considers the agreed functional scope of the student project, US-01–US-17, accepted. The application includes the core support-ticket workflow, AI chat, document-retrieval-based RAG, a bilingual interface, and a reproducible Docker Compose development/demo environment.

**Acceptance applies to the agreed functional scope of the student project and the documented local test environment. It does not mean that the application is ready for production use on a LAN or WAN, nor that it has undergone an independent security audit.**
