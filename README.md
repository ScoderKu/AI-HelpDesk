# AI HelpDesk

AI HelpDesk is a bilingual (Finnish/English) technical-support web application. Users can ask an AI assistant about IT and software-development issues, manage their own support tickets, and review saved conversations.

## Features

- User registration, sign-in, sign-out and profile management.
- AI chat with saved conversation history, retry for unanswered messages and Stop Generation.
- Independent conversations and child conversations with a user-reviewed title and context summary.
- Ticket creation, listing, editing of open tickets, and closing.
- Ticket creation from a conversation only after the user reviews and confirms the proposed title and description.
- A dashboard showing the signed-in user's total, OPEN and CLOSED ticket counts.
- Finnish and English interface.
- Project-specific RAG over an approved local Markdown/TXT knowledge corpus.
- Docker Compose development/demo environment with MySQL, Redis and Ollama.

## Technology

| Layer | Technology |
|---|---|
| Frontend | React 19, TypeScript, Vite |
| Backend | Python, FastAPI, Uvicorn |
| Database and migrations | MySQL 8.4, SQLAlchemy, Alembic |
| Shared coordination and rate limiting | Redis |
| Local AI runtime | Ollama |
| Development environment | Docker Compose |

## Documentation

The maintained project documentation is available in both languages:

- [Documentation index (English and Finnish)](docs/README.md)
- [Project acceptance and verification report](reports/PROJECT_ACCEPTANCE_REPORT.md)
- [System design (EN)](docs/en/03-System%20Design.md) · [Järjestelmän suunnittelu (FI)](docs/fi/03-järjestelmän%20suunnittelu.md)
- [Security and deployment (EN)](docs/en/08-security-deployment-considerations.md) · [Tietoturva ja käyttöönotto (FI)](docs/fi/08-tietoturva-ja-kayttoonotto.md)

The documentation index explains which document is authoritative for requirements, user stories, design, planning, licensing and verification. Source code, configuration and database migrations define the implemented behavior.

## Prerequisites

- Docker Engine/Desktop with Docker Compose.
- NVIDIA GPU support is used by the current Compose configuration. Other GPU types have not been validated.
- Sufficient disk space for the Ollama model and Docker images.

## Local setup

1. Clone the repository and open its root directory.
2. Create a local environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

3. Set unique database passwords and generate a unique 64-character JWT_SECRET_KEY for this environment:

   ```powershell
   [Convert]::ToHexString([Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
   ```

   Paste the generated value into .env. Do not commit .env or reuse production secrets.

4. Keep the default model settings in .env unless you have selected and tested another Ollama-compatible model:

   ```dotenv
   OLLAMA_MODEL=poro
   OLLAMA_MODEL_SOURCE=modelfile
   ```

   The default Modelfile expects ollama/models/Llama-Poro-2-8B-Instruct.Q4_K_M.gguf. Check model licensing and hardware requirements before use. If you change the model, keep OLLAMA_MODEL consistent for backend and model initialization.

5. Build and start the services:

   ```powershell
   docker compose up --build
   ```

6. Open the application at [http://localhost:8088](http://localhost:8088). phpMyAdmin is available locally at [http://localhost:8080](http://localhost:8080).

The first startup downloads the container images and initializes the configured Ollama model. The model is stored in the persistent ollama_data volume. Backend startup waits for required services and model preload.

## Basic usage

1. Register an account or sign in.
2. Create or manage support tickets in the ticket view.
3. Start an independent chat from New Conversation. To continue an existing chat as a child, use New Child Conversation when the context-usage rule enables it; review and confirm the proposed title and summary.
4. Create a ticket from a chat only after reviewing and confirming the AI-proposed details.
5. Change the interface language between Finnish and English.

## Development checks

Run frontend checks from the frontend/ directory:

```powershell
npm run lint
npm run build
```

Run backend unit tests from the project root:

```powershell
docker compose exec backend python -m unittest discover -s tests -v
```

The acceptance report records historical test evidence and explicitly lists checks that remain unverified. These results must not be interpreted as a fresh test run for the current commit.

## Deployment boundary

The supplied Compose configuration binds published service ports to loopback for local development/demo use. It is not a production deployment configuration. Do not expose the application directly to the public Internet. Review the bilingual Security and Deployment documentation and complete a separate deployment/security review before LAN or WAN exposure.

## License

The project's own license has not yet been selected. Third-party dependency and model licensing is under review; see document 07 in the documentation index.
