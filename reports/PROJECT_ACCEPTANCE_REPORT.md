# AI HelpDesk – Project Acceptance and Verification Report

**Report date:** 16 November 2026  
**Repository baseline reviewed:** `main` at `f4b7478204a16f178ee0272f64b9f8c25271b837`  
**Purpose:** Consolidated record of project scope, implementation evidence reported during development, test results, known limitations, and acceptance boundaries.

> This report consolidates developer-reported test evidence and repository documentation. It is not an independent audit, penetration test, or guarantee of production readiness. Historical test counts are tied to their recorded dates and must not be interpreted as a fresh test run on the report date.

## 1. Project outcome

AI HelpDesk is a bilingual (Finnish/English) web-based technical support application. It combines user accounts and profile management, user-owned support tickets, AI-assisted technical conversations, conversation history, a limited document-based RAG workflow, and a Docker Compose development/demo environment.

**Technology baseline**
- Frontend: React 19, TypeScript, Vite
- Backend: Python, FastAPI, Uvicorn
- Persistence: MySQL 8.4 and SQLAlchemy/Alembic
- Shared coordination and rate limiting: Redis
- Local AI runtime: Ollama, with a configurable local model
- Development/demo orchestration: Docker Compose

The application is intended for a local development and demonstration environment. LAN/WAN production deployment is not accepted or security-validated.

## 2. Implemented functional scope

The repository and project records describe the following delivered areas:

- User registration, login/logout, server-side sessions and profile editing.
- User-owned support-ticket creation, listing, priority and status handling.
- AI chat with persisted user/assistant messages, clarifying questions, retry handling and response-language behavior.
- Ticket drafting from a conversation: the AI proposes a title and concise description, and the user reviews and confirms before creation.
- Dashboard totals for the user's tickets, including OPEN and CLOSED counts.
- Finnish and English interface text.
- Keyword-based RAG over a bounded Markdown/TXT knowledge collection, with source grounding and source display.
- Docker Compose startup for frontend, backend, MySQL, Redis and Ollama.
- Independent conversations and child conversations. A child has a parent reference and a persisted context-summary snapshot; the user can edit the AI-proposed title and summary before confirming creation. Parent messages are not copied into the child transcript.
- Context-usage indicator and child-conversation action based on the latest completed generation's usage measurement.
- Stop Generation behavior intended to cancel actual backend inference and discard the unfinished assistant response while retaining user messages.

The child-conversation workflow was added after the original Sprint plan and documented as an extension of US-06/US-08, not as a retroactive change to the original Story Point estimate.

## 3. Verification evidence and test history

### 3.1 Backend automated tests

| Date / change | Reported result | Interpretation |
|---|---|---|
| 03.11.2026 | 57 backend unittest tests passed | Historical test snapshot recorded in README/project management. |
| 05.11.2026 | 85 of 86 backend tests passed; one opt-in MySQL integration test skipped in the standard run | The separately invoked registration + eight concurrent MySQL sign-in integration test was reported as passing. |
| PR #21 follow-up, before 13.11.2026 | 84 backend tests passed after the reported fixes | User reported the test suite passed and merged the fixes to main. This is a later test baseline than the 05.11 snapshot; it is not a claim that 84 is the current total test count. |

These are historical developer-reported results. No fresh test command was executed as part of this report update. The exact current test count and status must be re-established from a fresh run before a new release.

### 3.2 Frontend checks

- Frontend production build was reported successful on Windows.
- Frontend lint was reported successful in Docker.
- TypeScript checks were reported successful in the 05.11.2026 verification snapshot.
- Windows host lint execution was affected by Windows Code Integrity / Smart App Control blocking the unsigned Oxlint native binding; lint was therefore run in Docker. This is an environment constraint, not evidence of a source lint failure.

No new frontend commands were run for this report.

### 3.3 Docker and database integration

Project records report:
- A clean Docker Compose startup with empty MySQL and Ollama volumes.
- MySQL and Redis health checks passing in the local Compose environment.
- A separate MySQL integration test for registration and eight concurrent logins passing.
- Database URL construction corrected to use SQLAlchemy `URL.create()`, avoiding parsing issues with special characters in credentials.
- Alembic migrations through `0008_conversation_tree.py` documented in the current main baseline.

These statements describe previously reported local development checks; they do not establish successful deployment on another host or on a production network.

### 3.4 Conversation lifecycle verification

On 13.11.2026, the developer reported successful manual functional testing of:
- starting an independent conversation from the sidebar;
- starting a child conversation through the separate continuation flow;
- editing and confirming the generated title and context summary;
- preserving the parent/child relationship and using the saved summary as child context.

Frontend build passed on Windows and lint passed in Docker in that work session.

The following were explicitly not claimed as fully verified:
- exact 70% boundary behavior and all missing/invalid measurement cases;
- every API error path and ownership edge case;
- every migration upgrade/downgrade scenario;
- multi-worker or multi-replica cancellation behavior;
- production runtime behavior with every Ollama image/version.

### 3.5 AI and RAG quality checks

The project team performed practical Finnish/English AI and RAG acceptance checks. An initial RAG test produced weakly related source material and an incorrect answer; the knowledge corpus and response handling were subsequently adjusted, and the developer reported the practical US-15 retest as accepted.

RAG is a limited keyword-search implementation, not a guarantee that every relevant document will be found. The local model can produce incorrect or unsupported content. Source citations must reflect retrieved source IDs and must not be invented.

## 4. Security and deployment assessment

The code and security documentation describe controls including:
- server-side sessions stored in MySQL and signed cookies;
- scrypt password hashing;
- Redis-backed login throttling and registration rate limiting;
- origin/CORS checks;
- owner-scoped ticket and conversation access;
- AI generation coordination through Redis;
- private API response cache controls and baseline browser security headers;
- Compose host-port bindings restricted to loopback for the local demo, with MySQL/Redis not published as host ports.

These controls do not constitute a complete security assessment.

**Not validated / not included in acceptance:**
- production LAN deployment using two physical devices and the intended HTTPS reverse proxy;
- public WAN exposure;
- a complete two-user IDOR test matrix for all protected resources;
- independent penetration testing or formal security certification;
- production container hardening, full dependency/image pinning, complete CSP, production OpenAPI restrictions, and operational monitoring;
- backup restoration and incident-response exercises;
- load and resilience testing for all AI cancellation, overload and timeout conditions.

The system should not be exposed directly to the public Internet. Follow the separate Security and Deployment document before any LAN/WAN deployment.

## 5. Licensing and distribution

The third-party license review is preliminary. Open items include selecting a project license, recording the exact model artifact source/revision/checksum and applicable model notices, confirming Redis 7.4 license terms for the intended use, and producing a complete dependency/container SBOM and notices for the release artifacts. This report is not legal advice.

## 6. Acceptance statement

The developer recorded practical acceptance of the agreed user stories US-01–US-17 on 05.11.2026. The subsequent conversation-lifecycle work was documented and reported manually tested on 13.11.2026.

Acceptance is limited to the agreed student-project functional scope and the reported local development/demo environment. It does **not** mean:
- the current main branch was freshly regression-tested on 16.11.2026;
- the system is production-ready;
- LAN or WAN deployment has been verified;
- AI answers are always correct;
- licensing obligations are fully closed;
- an independent security audit has been completed.

## 7. Recommended final handover checklist

- [ ] Run the complete backend test suite on the exact final commit and save the command/output.
- [ ] Run frontend lint, type-check and production build on the exact final commit.
- [ ] Run the MySQL integration test against the intended Compose stack.
- [ ] Verify fresh Compose startup and health checks.
- [ ] Re-test Stop Generation against the exact pinned Ollama image and confirm a subsequent generation succeeds.
- [ ] Verify conversation tree creation, parent ownership, persisted summary reuse and deletion behavior.
- [ ] Record exact boundary/error tests for context usage and child action visibility.
- [ ] Review environment variables, secrets, migrations and backup/restore procedure.
- [ ] Close model/dependency/container license inventory actions before redistribution.
- [ ] Keep LAN/WAN deployment explicitly out of scope unless a separate deployment and security task is approved.

---
# AI HelpDesk – Projektin hyväksyntä- ja testausraportti

**Raportin päiväys:** 16.11.2026  
**Tarkasteltu repositorion lähtötila:** `main`, commit `f4b7478204a16f178ee0272f64b9f8c25271b837`  
**Tarkoitus:** Koota yhteen projektin laajuus, kehityksen aikana raportoidut toteutus- ja testausnäytöt, tunnetut rajoitteet sekä hyväksynnän rajat.

> Raportti kokoaa kehittäjän ilmoittamia testituloksia ja repositorion dokumentaatiota. Se ei ole riippumaton auditointi, tunkeutumistestaus eikä takuu tuotantovalmiudesta. Historialliset testimäärät liittyvät ilmoitettuihin ajankohtiin, eivätkä tarkoita uutta testiajoa raportin päiväyksenä.

## 1. Projektin lopputulos

AI HelpDesk on suomen- ja englanninkielinen verkkopohjainen teknisen tuen sovellus. Se yhdistää käyttäjätilit ja profiilin hallinnan, käyttäjän omat tukipyynnöt, tekoälyavusteiset keskustelut, keskusteluhistorian, rajatun dokumenttipohjaisen RAG-toiminnon sekä Docker Compose -kehitys- ja esittely-ympäristön.

**Teknologinen perusta**
- Frontend: React 19, TypeScript ja Vite
- Backend: Python, FastAPI ja Uvicorn
- Tallennus: MySQL 8.4 sekä SQLAlchemy/Alembic
- Jaettu koordinointi ja käyttörajoitukset: Redis
- Paikallinen tekoälyajoympäristö: Ollama ja konfiguroitava paikallinen malli
- Kehitys- ja esittely-ympäristön orkestrointi: Docker Compose

Sovellus on tarkoitettu paikalliseen kehitys- ja esittelykäyttöön. LAN/WAN-tuotantokäyttöönottoa ei ole hyväksytty eikä tietoturvavarmennettu.

## 2. Toteutettu toiminnallinen laajuus

Repositorion ja projektin kirjaukset kuvaavat seuraavat toimitetut kokonaisuudet:

- Käyttäjän rekisteröityminen, kirjautuminen ja uloskirjautuminen, palvelinpuolen istunnot sekä profiilin muokkaus.
- Käyttäjän omien tukipyyntöjen luominen, listaus, prioriteetti ja tilanhallinta.
- AI-chat, tallennetut käyttäjän ja tekoälyn viestit, tarkentavat kysymykset, uudelleenyritys sekä vastauskielen käsittely.
- Tukipyynnön luonnostelu keskustelusta: tekoäly ehdottaa otsikkoa ja tiivistä kuvausta, ja käyttäjä tarkistaa ja vahvistaa luonnin.
- Käyttäjän tukipyyntöjen kokonaismäärä sekä OPEN- ja CLOSED-määrät etusivulla.
- Suomen- ja englanninkielinen käyttöliittymä.
- Avainsanahaku rajatusta Markdown/TXT-tietopohjasta sekä lähteiden käyttö ja näyttäminen.
- Docker Compose -käynnistys frontendille, backendille, MySQL:lle, Redisille ja Ollamalle.
- Itsenäiset keskustelut ja lapsikeskustelut. Lapsikeskusteluun tallennetaan emokeskusteluviittaus ja kontekstiyhteenvedon tilannekuva; käyttäjä voi muokata tekoälyn ehdottamaa otsikkoa ja yhteenvetoa ennen luonnin vahvistamista. Emokeskustelun viestejä ei kopioida lapsikeskustelun viestihistoriaan.
- Kontekstin käyttöasteen ilmaisin ja viimeisimmän valmistuneen generoinnin käyttömittaukseen perustuva jatkokeskustelutoiminto.
- Generoinnin pysäytystoiminto, jonka tarkoituksena on keskeyttää varsinainen backend-generointi ja hylätä keskeneräinen tekoälyvastaus käyttäjän viestien säilyessä.

Lapsikeskustelutoiminto lisättiin alkuperäisen Sprint-suunnitelman laatimisen jälkeen ja dokumentoitiin US-06/US-08-kokonaisuuden laajennuksena. Alkuperäistä Story Point -arviota ei muutettu jälkikäteen.

## 3. Testausnäyttö ja testihistoria

### 3.1 Backendin automaattitestit

| Päiväys / muutos | Ilmoitettu tulos | Tulkinta |
|---|---|---|
| 03.11.2026 | 57 backendin unittest-testiä läpäisi | README:hen ja projektinhallintaan kirjattu historiallinen testitilanne. |
| 05.11.2026 | 86 backend-testistä 85 läpäisi; yksi valinnainen MySQL-integraatiotesti ohitettiin normaalissa ajossa | Erikseen ajettu rekisteröitymisen ja kahdeksan rinnakkaisen MySQL-kirjautumisen integraatiotesti ilmoitettiin läpäistyksi. |
| PR #21:n jatkokorjaukset ennen 13.11.2026 | 84 backend-testiä läpäisi | Käyttäjä ilmoitti testisarjan läpäisseen ja yhdisti korjaukset main-haaraan. Tämä on myöhempi testauspohja kuin 05.11. tilanne; 84 ei ole väite nykyisestä testien kokonaismäärästä. |

Tulokset ovat historiallisia, kehittäjän ilmoittamia testiajoja. Raportin päivityksen yhteydessä ei suoritettu uutta testikomentoa. Nykyinen testimäärä ja tulos on selvitettävä uudella testiajolla ennen uutta julkaisua.

### 3.2 Frontendin tarkistukset

- Frontendin tuotantobuild ilmoitettiin onnistuneeksi Windowsissa.
- Frontendin lint ilmoitettiin onnistuneeksi Dockerissa.
- TypeScript-tarkistukset ilmoitettiin onnistuneiksi 05.11.2026 testaushetkellä.
- Windows-isännän lint-ajoon vaikutti Windows Code Integrity / Smart App Control, joka esti allekirjoittamattoman Oxlint-natiivikirjaston suorittamisen. Lint ajettiin tämän vuoksi Dockerissa. Tämä on kehitysympäristön rajoite, ei näyttö lähdekoodin lint-virheestä.

Tätä raporttia varten ei ajettu uusia frontend-komentoja.

### 3.3 Docker ja tietokantaintegraatio

Projektin kirjauksissa ilmoitetaan:
- Docker Compose -kokonaisuuden puhdas käynnistys tyhjillä MySQL- ja Ollama-volyymeilla.
- MySQL:n ja Redis-palvelun terveystarkistusten onnistuminen paikallisessa Compose-ympäristössä.
- Erillisen rekisteröitymisen ja kahdeksan samanaikaisen kirjautumisen MySQL-integraatiotestin onnistuminen.
- Tietokantayhteyden muodostuksen korjaus SQLAlchemy `URL.create()`-toiminnolla, jotta erikoismerkit tunnuksissa eivät rikkoneet URL-jäsennystä.
- Alembic-migraatiot aina tiedostoon `0008_conversation_tree.py` asti nykyisessä main-lähtötilassa.

Nämä ovat aiemmin raportoitujen paikallisten kehitysympäristötestien tuloksia; ne eivät osoita käyttöönoton onnistumista toisella palvelimella tai tuotantoverkossa.

### 3.4 Keskustelun elinkaaren testaus

13.11.2026 kehittäjä ilmoitti testanneensa manuaalisesti onnistuneesti:
- itsenäisen keskustelun aloittamisen sivupalkista;
- lapsikeskustelun aloittamisen erillisellä jatkamistoiminnolla;
- tekoälyn luoman otsikon ja kontekstiyhteenvedon muokkaamisen ja vahvistamisen;
- emo-/lapsisuhteen säilymisen ja tallennetun yhteenvedon käytön lapsikeskustelun kontekstina.

Frontendin build onnistui Windowsissa ja lint Dockerissa kyseisessä työskentelyvaiheessa.

Seuraavia asioita ei nimenomaisesti väitetty kokonaan varmennetuiksi:
- täsmälleen 70 prosentin raja sekä kaikki puuttuvan/virheellisen mittaustiedon tapaukset;
- kaikki API-virhepolut ja omistajuuden reunatapaukset;
- kaikki migraatioiden upgrade/downgrade-skenaariot;
- usean backend-työntekijän tai replikan keskeytystoiminta;
- tuotantoajon toiminta kaikilla Ollama-kuvaversioilla.

### 3.5 Tekoälyn ja RAG:n laatutarkistukset

Projektissa tehtiin suomen- ja englanninkielisiä AI- ja RAG-hyväksymistarkistuksia. Alkuperäinen RAG-testi palautti heikosti liittyvää lähdemateriaalia ja virheellisen vastauksen. Tietopohjaa ja vastausten käsittelyä muutettiin tämän jälkeen, ja kehittäjä ilmoitti US-15:n käytännön uusintatestin hyväksytyksi.

RAG on rajattu avainsanahaku, eikä se takaa kaikkien olennaisten dokumenttien löytymistä. Paikallinen malli voi tuottaa virheellistä tai lähteillä tukematonta sisältöä. Lähdeviitteiden on perustuttava todellisuudessa haettuihin lähdetunnisteisiin; niitä ei saa keksiä.

## 4. Tietoturva- ja käyttöönottoarvio

Koodi ja tietoturvadokumentaatio kuvaavat muun muassa seuraavia kontrolleja:
- MySQL:ään tallennetut palvelinpuolen istunnot ja allekirjoitetut evästeet;
- scrypt-salasanatiivisteet;
- Redis-pohjainen kirjautumisen ja rekisteröitymisen käyttörajoitus;
- Origin/CORS-tarkistukset;
- tukipyyntöjen ja keskustelujen omistajuuteen perustuvat haut;
- AI-generoinnin koordinointi Redisillä;
- yksityisten API-vastausten välimuistirajoitukset ja selaimen perustason tietoturvaotsakkeet;
- paikallisessa demossa Composen host-porttien sitominen loopback-osoitteisiin sekä MySQL:n/Redisin host-porttien julkaisematta jättäminen.

Nämä kontrollit eivät muodosta täydellistä tietoturva-arviointia.

**Ei varmennettu / ei sisälly hyväksyntään:**
- tuotantomainen LAN-käyttö kahdella fyysisellä laitteella ja tarkoitetulla HTTPS-reverse-proxyllä;
- julkinen WAN-julkaisu;
- kaikkien suojattujen resurssien täydellinen kahden käyttäjän IDOR-testimatriisi;
- riippumaton tunkeutumistestaus tai virallinen tietoturvasertifiointi;
- tuotantokonttien kovennus, riippuvuuksien ja kuvien täydellinen versiolukitus, kattava CSP, tuotannon OpenAPI-rajoitukset ja operatiivinen valvonta;
- varmuuskopion palautusharjoitus ja poikkeamatilanteiden toimintaharjoitus;
- kaikkien AI-keskeytys-, ylikuormitus- ja aikakatkaisutilanteiden kuormitus- ja palautumistestaus.

Sovellusta ei pidä julkaista suoraan julkiseen Internetiin. Noudata erillistä Tietoturva ja käyttöönotto -dokumenttia ennen LAN/WAN-käyttöönottoa.

## 5. Lisenssit ja jakelu

Kolmansien osapuolten lisenssiselvitys on alustava. Avoimia asioita ovat projektin oman lisenssin valinta, malliartefaktin tarkan lähteen/version/tarkistussumman ja malliin liittyvien ilmoitusten kirjaaminen, Redis 7.4 -lisenssiehtojen soveltuvuuden varmistaminen sekä täydellisen riippuvuus-/kontti-SBOM:n ja jakeluilmoitusten tuottaminen. Tämä raportti ei ole oikeudellinen lausunto.

## 6. Hyväksyntälausuma

Kehittäjä kirjasi käyttäjätarinoiden US-01–US-17 käytännön hyväksynnän 05.11.2026. Myöhempi keskustelun elinkaaren toteutus dokumentoitiin ja ilmoitettiin manuaalisesti testatuksi 13.11.2026.

Hyväksyntä koskee sovittua opiskelijaprojektin toiminnallista laajuutta ja raportoitua paikallista kehitys-/esittely-ympäristöä. Se **ei** tarkoita, että:
- nykyinen main-haara olisi testattu uudella täydellä regressioajolla 16.11.2026;
- järjestelmä olisi tuotantovalmis;
- LAN- tai WAN-käyttöönotto olisi varmennettu;
- tekoälyn vastaukset olisivat aina oikein;
- lisenssivelvoitteet olisi kokonaan ratkaistu;
- riippumaton tietoturva-auditointi olisi tehty.

## 7. Suositeltu lopullisen luovutuksen tarkistuslista

- [ ] Aja koko backend-testisarja täsmälleen lopullisella commitilla ja tallenna komento/tuloste.
- [ ] Aja frontendin lint, tyyppitarkistus ja tuotantobuild täsmälleen lopullisella commitilla.
- [ ] Aja MySQL-integraatiotesti tarkoitetussa Compose-ympäristössä.
- [ ] Varmista puhdas Compose-käynnistys ja palvelujen terveystarkistukset.
- [ ] Testaa Stop Generation täsmälleen käytössä olevalla lukitulla Ollama-kuvalla ja varmista, että seuraava generointi onnistuu.
- [ ] Varmista keskustelupuun luonti, emokeskustelun omistajuus, yhteenvedon tallennus ja uudelleenkäyttö sekä poistokäyttäytyminen.
- [ ] Kirjaa kontekstin käyttöasteen ja jatkokeskustelutoiminnon tarkat raja-arvo- ja virhetilannetestit.
- [ ] Tarkista ympäristömuuttujat, salaisuudet, migraatiot ja varmuuskopioiden palautusmenettely.
- [ ] Sulje mallien, riippuvuuksien ja konttikuvien lisenssi-inventoinnin avoimet toimet ennen jakelua.
- [ ] Pidä LAN/WAN-käyttöönotto erillisen hyväksytyn käyttöönotto- ja tietoturvatehtävän ulkopuolella.
