# AI HelpDesk — Product Overview

- **Document ID:** KB-PROJECT-00
- **Status:** verified project facts; status snapshot dated 2026-11-04
- **RAG Scope:** project-specific
- **Applies to:** AI HelpDesk repository
- **Keywords:** AI HelpDesk, helpdesk, support ticket, technical support, opiskelijaprojekti, tukipyyntö, tekninen tuki, project scope, requirements

## Product purpose

AI HelpDesk is a web application for helping users investigate IT and software-development problems. A signed-in user can describe a technical issue in an AI conversation, receive troubleshooting suggestions, revisit saved conversations, and create or manage support tickets.

The application is an educational project. Its agreed scope is intentionally smaller than an enterprise IT service-management platform.

## Main user capabilities

- Register, sign in and sign out.
- View profile information and change the username.
- Change the account password.
- Chat with a locally hosted AI model.
- Save and revisit conversations and messages.
- Create, view, update permitted fields of, and close the user's own support tickets.
- Create a ticket from a conversation only after reviewing and confirming the proposed title and description (US-09).
- View a limited summary of the user's ticket totals, including OPEN and CLOSED counts (US-14).
- Use Finnish or English UI text (US-13).

First name, last name and email are read-only in the profile. Username is the editable profile field. Ticket states in the current MVP are OPEN and CLOSED; priorities are LOW, MEDIUM and HIGH.

## Technology stack verified in the repository

- Frontend: React and TypeScript, built with Vite.
- Backend: Python and FastAPI, served by Uvicorn.
- Relational database: MySQL, configured for MySQL 8.4 in the project environment.
- ORM and migrations: SQLAlchemy and Alembic.
- Redis: login-attempt rate limiting and conversation-generation locking.
- AI runtime: Ollama.
- Model artifact: `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`, exposed to the backend under the model name `poro-helpdesk`.
- Runtime/orchestration: Docker Compose.
- Frontend package manager: npm.

The project aims to use free-of-charge tools and libraries. A free-to-use price does not automatically mean unrestricted licensing; model, library and tool licences must be checked before distribution.

## Agreed scope and exclusions

RAG (US-15) uses a curated Markdown/TXT corpus with keyword search first. The initial implementation is on PR #21 (`feature/us15-rag-knowledge-service`) and is not yet merged into `main`. The live corpus is restricted to project-specific AI HelpDesk knowledge. General programming and computer knowledge is handled by the model directly and is kept outside the searchable corpus. Semantic search is not part of the MVP unless tests show keyword search is insufficient.

The project does not promise:
- voice input or spoken responses;
- automatic execution of commands on the user's computer;
- fully autonomous repair without user participation;
- university single sign-on;
- broad enterprise ITSM workflows or cross-organization permissions;
- PDF report generation.

## Operational and safety boundaries

- The AI can explain and suggest commands, but it must not claim it has executed them.
- The AI must not request passwords, one-time codes, tokens or other secrets.
- The AI must not claim to have created a ticket. Ticket creation is a separate application action requiring the user's review and confirmation.
- Users may access only their own tickets, conversations and messages.
- The project has a data-retention task that permanently deletes eligible closed tickets and inactive conversations after three calendar months. This is not an archive/undo feature.

## Status caveat

The repository README snapshot dated 2026-11-03 says registration/sign-in, tickets, AI chat and conversation history are connected to the backend; it reports 57 backend tests and frontend lint/build checks passing in the then-current local working tree. Sprint 4–5 work and full acceptance testing were still in progress. Do not infer that RAG is already implemented: README explicitly says it is planned Sprint 5 work.


## Tiivistelmä suomeksi

AI HelpDesk on IT- ja ohjelmistokehitysongelmien selvittämiseen tarkoitettu verkkosovellus. Kirjautunut käyttäjä voi keskustella tekoälyn kanssa, tarkastella keskusteluhistoriaa sekä luoda ja hallita tukipyyntöjä. Kyseessä on rajattu opiskelijaprojekti, ei täysimittainen ITSM-järjestelmä. Käyttöoikeudet ja tietojen omistajuus tarkistetaan backendissä. Projektin ominaisuuksien toteutustila on tarkistettava nykyisestä lähdekoodista; suunnitelmaa ei saa sekoittaa valmiiseen ominaisuuteen.
