# AI HelpDesk — Source-Code Audit: API, Data Model and Compose

- **Document ID:** KB-PROJECT-21
- **Status:** verified by reading `backend/app/main.py`, `backend/app/models.py` and `compose.yaml` on 2026-11-04
- **Applies to:** current repository default-branch source inspected on the date above
- **Keywords:** API routes, endpoint, SQLAlchemy model, MySQL schema, Compose service, Docker network, rajapinta, tietokantamalli, palvelut

## 1. API routes observed in backend/app/main.py

The following route paths were present in the inspected source. HTTP methods are shown explicitly; this list is not a substitute for request/response schemas.

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/auth/register` | Register account |
| POST | `/api/v1/auth/login` | Sign in |
| POST | `/api/v1/auth/logout` | Sign out |
| GET | `/api/v1/auth/me` | Current authentication state |
| GET | `/api/v1/users/me` | Read own profile |
| PATCH | `/api/v1/users/me` | Update own profile |
| POST | `/api/v1/users/me/password` | Change own password |
| GET | `/api/v1/tickets` | List own tickets |
| POST | `/api/v1/tickets` | Create ticket |
| GET | `/api/v1/tickets/summary` | Own ticket totals/status summary |
| GET | `/api/v1/tickets/{ticket_id}` | Read ticket |
| PATCH | `/api/v1/tickets/{ticket_id}` | Update ticket |
| POST | `/api/v1/tickets/{ticket_id}/close` | Close ticket |
| GET | `/api/v1/conversations` | List own conversations |
| POST | `/api/v1/conversations` | Create conversation |
| GET | `/api/v1/conversations/{conversation_id}` | Read conversation |
| GET | `/api/v1/conversations/{conversation_id}/messages` | List messages |
| POST | `/api/v1/conversations/{conversation_id}/ticket-draft` | Generate ticket draft |
| POST | `/api/v1/conversations/{conversation_id}/tickets` | Create ticket from conversation after confirmation |
| POST | `/api/v1/conversations/{conversation_id}/messages/stream` | Stream AI response |
| POST | `/api/v1/conversations/{conversation_id}/messages` | Send non-streaming chat message |
| POST | `/api/v1/conversations/{conversation_id}/messages/{message_id}/retry` | Retry assistant response |
| GET | `/api/v1/ai/health` | Authenticated Ollama health check |
| GET | `/api/health` | Backend health |
| GET | `/api/health/db` | Database health |

**FI:** Nämä reitit on luettu backendin nykyisestä `main.py`-tiedostosta tarkistushetkellä. Tarkista aina myös Pydantic-skeemat, käyttöoikeustarkistukset ja testit ennen asiakkaan tai integraation muuttamista. Reitin olemassaolo ei yksin tarkoita, että käyttäjällä olisi oikeus käyttää sitä kaikkiin tietoihin.

## 2. SQLAlchemy entities observed in backend/app/models.py

| Table | Important fields and constraints |
|---|---|
| `users` | BigInteger primary key; first_name, last_name, username (unique), email (unique), password_hash, must_change_password, created_at, updated_at |
| `auth_sessions` | String(32) primary key; user_id FK to users with CASCADE; expires_at indexed; created_at |
| `conversations` | BigInteger primary key; user_id FK to users with CASCADE; nullable title and response_language; created_at, updated_at; index on updated_at |
| `tickets` | BigInteger primary key; user_id FK to users with CASCADE; nullable conversation_id FK to conversations with SET NULL; title, description, status, priority, created_at, updated_at, nullable closed_at; index on (status, closed_at) |
| `messages` | BigInteger primary key; conversation_id FK to conversations with CASCADE; role, content, created_at; index on (conversation_id, created_at, id) |

**Important:** This table is a summary of ORM declarations, not a full MySQL DDL dump. Confirm the actual deployed schema with the migrations/database before changing it. Column types, nullability and FK delete behavior should be preserved unless a reviewed migration intentionally changes them.

**FI:** SQLAlchemy-mallit määrittelevät käyttäjät, istunnot, keskustelut, tukipyynnöt ja viestit. Käyttäjän poistaminen poistaa siihen liittyvät istunnot, keskustelut ja tukipyynnöt viiteavainten CASCADE-säännön mukaisesti. Keskustelun poistaminen asettaa siihen liittyvän tukipyynnön `conversation_id`-kentän NULL-arvoon, mutta poistaa keskustelun viestit. Tarkista migraatiot ja käytössä oleva MySQL-skeema ennen muutoksia.

## 3. Compose services observed in compose.yaml

| Service | Role | Important observed configuration |
|---|---|---|
| frontend | React/Vite development frontend | Dockerfile.hmr; host port 8088 bound to 127.0.0.1; proxy network address 172.30.0.2 |
| backend | FastAPI | host port 8000 bound to 127.0.0.1; connects to mysql, redis and ollama by service DNS; proxy alias backend-proxy at 172.30.0.3 |
| redis | Redis 7 Alpine | 128 MB maxmemory, no persistence, noeviction; redis-cli ping healthcheck |
| mysql | MySQL 8.4 | persistent mysql_data volume; healthcheck with mysqladmin |
| phpmyadmin | Database administration UI | host port 8080 bound to 127.0.0.1; connects to mysql |
| ollama | Local model runtime | host port 11434 bound to 127.0.0.1; persistent ollama_data; mounts ./ollama read-only; NVIDIA GPU reservation |
| ollama-model-init | Model initialization helper | waits for Ollama health, creates poro-helpdesk from /models/Modelfile if absent, exposes readiness healthcheck |

Compose defines a dedicated `proxy` network with subnet `172.30.0.0/24`. The frontend's API proxy target is `http://backend-proxy:8000`. Backend uses `mysql+pymysql` with MySQL service DNS, `redis://redis:6379/0`, and `http://ollama:11434`.

**Operational cautions**
- All listed host port bindings use loopback (127.0.0.1), so this Compose file does not expose these services to other LAN devices by default.
- The frontend service uses the HMR Dockerfile and Vite development server. Do not describe this Compose file as a production frontend build.
- Redis persistence is disabled in this Compose configuration; do not store durable user data only in Redis.
- Model initialization is a separate service. Backend startup depends on its healthy state.
- The compose file requests NVIDIA GPU resources for Ollama; actual GPU availability still depends on host drivers and Docker GPU support.
- The actual .env file is secret material and must never be copied into this corpus.

**FI:** Compose-tiedostossa on frontend, backend, Redis, MySQL, phpMyAdmin, Ollama ja mallin alustava palvelu. Isäntäkoneen portit on sidottu loopback-osoitteeseen, joten palvelut eivät oletusarvoisesti ole lähiverkon muiden laitteiden käytettävissä. Frontend käyttää kehityspalvelinta (Vite HMR), ei tuotantorakennetta. Redis ei tallenna tietoja pysyvästi. Ollaman mallin alustaminen tehdään erillisessä palvelussa ennen backendin käynnistymistä.

## 4. Review limitations

This audit directly inspected the three named source files. It did not execute Docker Compose, query the live MySQL schema, invoke every endpoint, or run the test suite. Treat runtime behavior as unverified unless a dated test result is separately recorded. The API table should be regenerated when routes change.

Tässä tarkistuksessa luettiin suoraan kolme nimettyä lähdetiedostoa. Docker Composea ei käynnistetty, käytössä olevaa MySQL-skeemaa ei kysytty, kaikkia rajapintoja ei kutsuttu eikä testisarjaa suoritettu. Ajonaikainen toiminta on vahvistamaton, ellei siitä ole erillistä päivättyä testitulosta.
