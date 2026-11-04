# AI HelpDesk — Backend API and Data Model

- **Document ID:** KB-PROJECT-02
- **Status:** verified against FastAPI source, SQLAlchemy models, schemas and project design at review time
- **Applies to:** `backend/app/main.py`, `models.py`, `schemas.py`, database migrations
- **Keywords:** FastAPI, REST API, endpoint, SQLAlchemy, Alembic, database, schema, data model, rajapinta, tietomalli, tietokanta

## Backend structure

The FastAPI application is created in `backend/app/main.py`. Important supporting modules include:
- `app/ai.py`: Ollama model preload, non-streaming AI calls, ticket-draft generation and streaming generation.
- `app/database.py`: SQLAlchemy engine, session factory and request-scoped database dependency.
- `app/models.py`: ORM entities.
- `app/schemas.py`: Pydantic request/response schemas and enums.
- `app/security.py`: password hashing and verification.
- `migrations/`: Alembic schema history.
- `tests/`: backend unit and API tests.

The exact module list may grow. Check the repository before relying on this inventory.

## Main API families

The API is versioned under `/api/v1`. The reviewed source contains these families:

### Authentication and profile
- `POST /api/v1/auth/login` — sign in.
- `GET /api/v1/auth/me` — check current authentication state.
- `POST /api/v1/auth/logout` — sign out; Origin must be trusted.
- `GET /api/v1/users/me` — read current profile.
- `PATCH /api/v1/users/me` — update permitted profile fields (username only).
- `POST /api/v1/users/me/password` — change password.

### Tickets
- `GET /api/v1/tickets` — list the authenticated user's tickets.
- `POST /api/v1/tickets` — create a ticket.
- Additional ticket detail/update/close routes are implemented in the backend; inspect OpenAPI or route decorators before relying on a complete route inventory.

### Conversations and messages
The project design and frontend use:
- `GET /api/v1/conversations`
- `POST /api/v1/conversations`
- `GET /api/v1/conversations/{conversation_id}`
- `GET /api/v1/conversations/{conversation_id}/messages`
- `POST /api/v1/conversations/{conversation_id}/messages/stream`
- `POST /api/v1/conversations/{conversation_id}/messages/{message_id}/retry`
- `POST /api/v1/conversations/{conversation_id}/ticket-draft`
- `POST /api/v1/conversations/{conversation_id}/tickets`

Always check the current backend decorators and OpenAPI schema before treating this list as a contractual API specification.

## Validation

Pydantic schemas validate data at the API boundary. The chat request schema currently strips surrounding whitespace, requires a non-empty message and limits it to 12,000 characters and 48,000 UTF-8 bytes. Request models use `extra="forbid"` in relevant schemas so unknown fields are rejected.

The backend returns HTTP 422 for request validation errors. The custom handler removes raw input values from validation details to reduce accidental exposure of submitted data.

## Data ownership

The backend derives the authenticated user from the validated session. It must not trust a client-supplied `user_id` to establish ownership. Ticket and conversation queries must filter by the authenticated user's ID. A user must not be able to read or modify another user's resources by changing an integer ID in the URL.

## Main entities

The current ORM model set includes:
- `User`
- `AuthSession`
- `Ticket`
- `Conversation`
- `Message`

Conceptual relationships:
- A user owns their tickets.
- A user owns their conversations.
- A conversation contains messages.
- A ticket created from a conversation can reference that conversation; independently created tickets have no conversation reference.

The exact SQL column types, constraints, indexes and delete rules are defined by `backend/app/models.py` and Alembic migrations. Read those files before writing SQL or changing the schema.

## Database access

`backend/app/database.py` constructs the MySQL SQLAlchemy URL using `URL.create()` with environment values. This avoids manual URL string escaping problems when a password contains reserved characters such as `#`. The current Compose database hostname is `mysql`, port 3306.

Use the `get_db` dependency for request-scoped sessions and close sessions reliably. Do not create a new database engine for each API request.

## Schema changes

Use Alembic migrations for schema changes. Review generated migrations manually. Back up the MySQL volume before applying migrations to important existing data. A schema change is not complete until migration-upgrade and relevant application tests have been checked.


## Tiivistelmä suomeksi

FastAPI määrittelee HTTP-reitit ja käsittelee pyynnöt. SQLAlchemy yhdistää Python-oliot relaatiotietokantaan, Pydantic validoi pyyntö- ja vastausrakenteita ja Alembic hallitsee tietokantamigraatioita. Keskeiset tietokäsitteet ovat käyttäjät, tukipyynnöt, keskustelut ja viestit. Käyttäjän omistajuus on tarkistettava jokaisessa luku- ja muutosoperaatiossa. Käytä taulujen ja kenttien tarkkoihin nimiin nykyisiä ORM-malleja ja migraatioita, älä vanhaa ER-kuvaa yksinään.
