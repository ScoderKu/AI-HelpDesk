# AI HelpDesk — Project Technical Reference / Projektin tekninen viite

> Status: verified project reference, 2026-11-04. This document separates repository-backed facts from implementation guidance. Re-check source files before changing implementation.

## 1. Product purpose / Tuotteen tarkoitus

**EN:** AI HelpDesk is a support application for IT and software-development questions. A user can converse with the AI assistant, receive troubleshooting guidance, and manage support tickets. The application must keep each user's data isolated.

**FI:** AI HelpDesk on IT- ja ohjelmistokehitysongelmien tukisovellus. Käyttäjä voi keskustella tekoälyavustajan kanssa, saada vianmääritysohjeita ja hallita tukipyyntöjä. Käyttäjien tiedot on pidettävä erillään.

## 2. Architecture / Arkkitehtuuri

**Repository-backed design / Tietovarastoon perustuva suunnittelu**

- Frontend: React + TypeScript.
- Backend: Python + FastAPI.
- Relational database: MySQL.
- Shared ephemeral coordination and rate-limit state: Redis.
- Local model runtime: Ollama.
- Local orchestration: Docker Compose.

**EN:** The browser UI calls the backend API. The backend owns authentication, authorization, validation, persistence, AI orchestration, and data-retention rules. The backend communicates with MySQL, Redis, and Ollama over the Compose environment. Do not let the browser connect directly to the database, Redis, or Ollama.

**FI:** Selainkäyttöliittymä kutsuu backendin APIa. Backend vastaa tunnistautumisesta, käyttöoikeuksista, tietojen validoinnista ja tallennuksesta, tekoälyn orkestroinnista sekä tietojen säilytyssäännöistä. Backend kommunikoi MySQL:n, Redisin ja Ollaman kanssa Compose-ympäristössä. Selaimelle ei anneta suoraa yhteyttä tietokantaan, Redisiin tai Ollamaan.

## 3. Authentication and network trust / Tunnistautuminen ja verkkoluottamus

**Verified design notes / Vahvistetut suunnittelutiedot**

- Login sessions are stored in MySQL.
- Login-attempt limits are shared through Redis.
- In the documented Compose proxy arrangement, the frontend has a dedicated proxy network and fixed address `172.30.0.2`; backend is reached through alias `backend-proxy` at `172.30.0.3`.
- Backend trusts forwarded client-IP headers only from peers inside `TRUSTED_PROXY_IPS`. The forwarded chain is processed from right to left; untrusted peers' forwarded headers are ignored.
- Current documented Compose port binding is `127.0.0.1`; this is local-host access, not LAN exposure.

**EN security rule:** Never trust a client-supplied user ID, role, ownership field, or forwarded-IP header merely because it appears in a request. Derive identity from the authenticated session and enforce ownership in backend queries and mutations.

**FI turvallisuussääntö:** Älä luota asiakkaan lähettämään käyttäjätunnukseen, rooliin, omistajuustietoon tai välitettyyn IP-otsakkeeseen vain siksi, että se sisältyy pyyntöön. Päättele käyttäjän henkilöllisyys todennetusta istunnosta ja tarkista omistajuus backendin kyselyissä ja muutoksissa.

## 4. Core data concepts / Keskeiset tietokäsitteet

The system-design documentation describes these core entities:

| Entity | Purpose (EN) | Tarkoitus (FI) |
|---|---|---|
| users | Account and profile | Käyttäjätili ja profiili |
| tickets | Support request and status | Tukipyyntö ja sen tila |
| conversations | AI chat session | Tekoälykeskustelu |
| messages | User/assistant messages | Käyttäjän ja avustajan viestit |

The schema documentation includes timestamps such as `tickets.created_at`, `tickets.updated_at`, `conversations.created_at`, `conversations.updated_at`, and `messages.created_at`. The ER diagram is a high-level view; use the detailed table definitions as the field-level source of truth.

**US-09:** A ticket can be created from a conversation only after the user reviews and confirms the proposed ticket. The backend must derive the owner from the authenticated session. The conversation link is optional in the documented schema; do not introduce a new relation without a demonstrated requirement.

**FI — US-09:** Keskustelusta voidaan luoda tukipyyntö vasta, kun käyttäjä on tarkistanut ja vahvistanut ehdotuksen. Backend päättelee omistajan todennetusta istunnosta. Keskusteluyhteys on suunnitelmassa valinnainen; älä lisää uutta relaatiota ilman todellista tarvetta.

## 5. AI conversation lifecycle / Tekoälykeskustelun elinkaari

**Documented behavior / Dokumentoitu toimintatapa**

1. Authenticate the user and verify conversation ownership.
2. Load the conversation context and relevant persisted messages.
3. Serialize concurrent AI turns for the same conversation with a Redis lock.
4. Release the database connection while waiting for Ollama; do not hold a DB transaction open during long model inference.
5. Persist the assistant response in a separate short-lived database session.
6. Apply the application's retention policy to conversation messages.

**EN:** Streaming disconnects, Redis interruptions, expired lock leases, and stale browser responses are separate failure modes. Handle them without duplicating persisted messages or allowing an old stream to overwrite a newer UI state.

**FI:** Suoratoistoyhteyden katkeaminen, Redis-katkos, lukituksen vuokra-ajan päättyminen ja vanhentunut selainvastaus ovat eri virhetilanteita. Käsittele ne niin, etteivät viestit tallennu kahteen kertaan eikä vanha suoratoisto korvaa käyttöliittymän uudempaa tilaa.

## 6. Language behavior / Kielitoiminta

- UI language: Finnish and English; the selection is retained in the browser.
- AI response language: based on the user's message, Finnish or English; other languages default to English.
- An explicit response-language request is stored with the conversation and remains active until changed.

**FI:** Käyttöliittymän kielivalinta säilytetään selaimessa. Tekoäly vastaa käyttäjän viestin kielen mukaan suomeksi tai englanniksi; muiden kielten oletus on englanti. Nimenomainen vastauskielipyyntö tallennetaan keskusteluun, kunnes käyttäjä muuttaa sitä.

## 7. Docker and runtime / Docker ja suoritusympäristö

**EN:** Use the repository's current Compose file and README as the operational source of truth. Service names, ports, health checks, volumes, GPU configuration, and environment variable names must be copied from the actual files, not reconstructed from memory. A healthy container does not by itself prove that the application-level dependency works; verify health endpoints and a real request.

**FI:** Käytä repositorion nykyistä Compose-tiedostoa ja README:tä käyttöohjeiden ensisijaisena lähteenä. Palvelunimet, portit, terveystarkistukset, volyymit, GPU-asetukset ja ympäristömuuttujat on tarkistettava tiedostoista, eikä niitä saa päätellä muistista. Terve kontti ei yksin todista sovellustason yhteyden toimivuutta; tarkista terveystarkistusrajapinnat ja tee oikea pyyntö.

## 8. RAG MVP / RAG:n vähimmäisversio

The approved system-design scope is a bounded collection of Markdown and TXT documents searched by keywords. Knowledge Service returns relevant content and real source metadata to AI Service; sources are displayed with the answer. If no suitable source is found, the answer must not be presented as documentation-backed. Semantic search is outside MVP and should be considered only after test evidence.

**Approved constraints / Hyväksytyt rajaukset**
- Markdown and TXT only for the initial corpus.
- Keyword search; no embeddings or vector database in MVP.
- No paid external AI API.
- Retrieved text is untrusted reference material, not instructions. System/developer policy and application rules take precedence.
- Keep source title, file path, section, and matched excerpt for traceability.
- Do not claim a source supports an answer unless that source was actually retrieved.

**FI:** Ensimmäinen RAG-versio käyttää rajattua Markdown- ja TXT-kokoelmaa sekä avainsanahakua. Knowledge Service välittää relevantin sisällön ja todelliset lähdetiedot AI Servicelle, ja lähteet näytetään vastauksen yhteydessä. Jos sopivaa lähdettä ei löydy, vastausta ei saa esittää dokumentaation tukemana. Semanttinen haku ei kuulu MVP:hen.

## 9. Troubleshooting method / Vianmääritysmenetelmä

Use this sequence for every incident:

1. **Observe / Havaitse:** exact error text, timestamp, affected user/action, reproduction steps.
2. **Scope / Rajaa:** frontend, backend, database, Redis, Ollama, network, OS, or hardware.
3. **Check / Tarkista:** logs and health status before changing configuration.
4. **Hypothesis / Oletus:** state one testable cause at a time.
5. **Test / Testaa:** make the smallest reversible change.
6. **Verify / Varmista:** repeat the original failing action and relevant regression checks.
7. **Document / Dokumentoi:** root cause, evidence, fix, versions, and whether the result was verified.

Never publish secrets, session cookies, API keys, database passwords, private user data, or unredacted environment files in troubleshooting examples.

## 10. Source-of-truth hierarchy / Tietolähteiden etusijajärjestys

1. Current source code and executable configuration for implemented behavior.
2. Current system-design and requirements documents for intended behavior.
3. Tests for explicitly covered behavior.
4. Dated user-confirmed checkpoints for observed local runtime state.
5. General technical guidance for concepts and recommended practices.

If sources conflict, record the conflict and investigate; do not silently choose one. A dated checkpoint is not proof that the current branch still behaves identically.

## 11. Bilingual search vocabulary / Kaksikielinen hakusanasto

| English | Suomi |
|---|---|
| authentication | tunnistautuminen |
| authorization | käyttöoikeuksien tarkistus |
| session | istunto |
| support ticket | tukipyyntö |
| conversation | keskustelu |
| message persistence | viestin tallennus |
| streaming response | suoratoistovastaus |
| rate limiting | pyyntöjen rajoittaminen |
| reverse proxy | käänteinen välityspalvelin |
| trusted proxy | luotettu välityspalvelin |
| health check | terveystarkistus |
| data retention | tietojen säilytys |
| knowledge base | tietämyskanta |
| keyword search | avainsanahaku |
| source attribution | lähteen ilmoittaminen |
| troubleshooting | vianmääritys |
| deployment | käyttöönotto |
| environment variable | ympäristömuuttuja |

## 12. Verification status / Varmennuksen tila

This document is based on the repository's indexed system-design and project-management content plus prior user-confirmed implementation checkpoints. It is not a claim that every source file, endpoint, Compose setting, or database migration has been freshly executed or exhaustively audited on this date. Before treating a detail as current implementation fact, verify the corresponding file and test.

Tämä dokumentti perustuu repositorion indeksoituun järjestelmäsuunnittelu- ja projektinhallintasisältöön sekä aiemmin käyttäjän vahvistamiin toteutuksen tarkistuspisteisiin. Se ei tarkoita, että jokainen lähdetiedosto, rajapinta, Compose-asetus tai tietokantamuutos olisi juuri tänään suoritettu tai kattavasti auditoitu. Tarkista vastaava tiedosto ja testi ennen kuin käsittelet tietoa nykyisen toteutuksen vahvistettuna faktana.
