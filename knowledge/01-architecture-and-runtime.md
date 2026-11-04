# AI HelpDesk — Architecture and Runtime

- **Document ID:** KB-PROJECT-01
- **Status:** architecture verified from repository README and backend/frontend source; Compose details should be checked against the current compose file before operational changes
- **Applies to:** full application
- **Keywords:** architecture, runtime, frontend, backend, API, MySQL, Redis, Ollama, Docker network, arkkitehtuuri, palvelurakenne, verkkoyhteys

## Component responsibilities

### Browser and React frontend

The browser loads the React application. React manages page state and renders authentication, home, tickets, profile and chat experiences. Frontend API requests use the configured API base URL and include browser credentials where session authentication is required.

### FastAPI backend

The backend is the trusted application boundary. It:
- validates incoming request data;
- identifies the signed-in user from the session cookie and MySQL session record;
- enforces ownership checks;
- implements ticket and conversation business rules;
- reads/writes MySQL through SQLAlchemy;
- uses Redis for rate limiting and chat-generation locks;
- calls Ollama for model inference.

The frontend must not be treated as the security boundary. Hiding a button does not authorize an operation; the backend must validate every protected action.

### MySQL

MySQL stores user accounts, authentication sessions, tickets, conversations and messages. SQLAlchemy models represent database entities and Alembic migrations manage schema evolution.

### Redis

Redis is not the system of record for user accounts or conversations. In the current backend it supports:
- shared login-attempt counters and expiry windows;
- per-conversation AI generation locks with expiring leases.

### Ollama

Ollama exposes a local HTTP API to the backend. The backend sends chat requests to Ollama using the configured model name. Ollama runs in the Compose environment according to the README's current architecture.

### Knowledge Service (planned RAG)

The planned Knowledge Service reads a curated local Markdown/TXT corpus, performs keyword retrieval, and supplies matching excerpts and source metadata to the AI prompt. The README depicts this component, but the reviewed backend source did not yet contain the knowledge-search implementation or a RAG API endpoint. Treat it as planned until code and tests prove otherwise.

## Request flow

Typical authenticated request:

1. Browser sends an HTTP request to the frontend's same-origin `/api` route or configured backend origin.
2. Frontend includes the session cookie when required.
3. Backend validates the cookie signature, expiry and corresponding active session in MySQL.
4. Backend validates the request schema and checks resource ownership.
5. Backend reads/writes MySQL or calls Redis/Ollama as required.
6. Backend returns JSON or a streaming response.
7. React updates the visible state from the response.

For a chat response, the backend also retrieves the required conversation history and sends role-labelled messages to Ollama. The streaming path emits application-level events to the browser.

## Compose networking concepts

A Docker Compose service should connect to another service using its Compose service name or configured network alias, not the host machine's `localhost`. Inside a container, `localhost` means that same container.

The README describes a dedicated frontend-to-backend proxy network. It identifies frontend proxy address `172.30.0.2`, backend proxy alias `backend-proxy`, and a backend trusted-proxy setting `TRUSTED_PROXY_IPS`. These values are deployment configuration, not universal Docker defaults. If the network or proxy address changes, the trusted proxy configuration must be reviewed too.

The README describes local HTTP development as loopback-bound and therefore not reachable from other LAN devices. Do not claim LAN access is enabled merely because the container ports are published.

## Health and readiness

Distinguish:
- **container running:** Docker process is alive;
- **health check passing:** configured health check succeeds;
- **application ready:** backend has completed its startup dependencies;
- **AI ready:** Ollama is reachable and the configured model can answer.

The backend lifespan currently pings Redis and repeatedly attempts Ollama model preload before serving. A running backend container alone does not prove Ollama inference is ready.

## Troubleshooting order

1. Check `docker compose ps` and health status.
2. Inspect the failing service logs with `docker compose logs --tail=100 <service>`.
3. Check environment variables without printing secret values.
4. Check service DNS and ports from the container that initiates the connection.
5. Check application health endpoints and API responses.
6. Check persistent volume state before considering destructive reset commands.

Never recommend `docker compose down -v` as a routine restart: `-v` removes named volumes and can delete MySQL or Ollama data.
