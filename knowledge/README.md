# AI HelpDesk — Project-Specific RAG Knowledge Base

**Purpose:** verified, project-specific technical knowledge for the AI HelpDesk local RAG feature.

**Scope decision (2026-11-04):** this directory is not a general programming or computer encyclopedia. The model answers common questions about Python, JavaScript, React, Windows, hardware and other general topics from its own learned knowledge. RAG is reserved for facts it cannot know reliably without this repository: this project's architecture, source code, API, database, configuration, AI integration, workflows and verified incident history.

## Included in RAG

Only Markdown/TXT documents explicitly marked with this front matter field are indexed:

`- **RAG Scope:** project-specific`

A document without this exact approval marker is not retrieved. This is enforced in `backend/app/knowledge.py`, not merely described here.

| File | Scope |
|---|---|
| 00-project-overview.md | Product scope, project stack and application-specific boundaries |
| 01-architecture-and-runtime.md | AI HelpDesk components, request flow, Compose networking and readiness |
| 02-backend-api-and-data.md | Project backend modules, endpoints, data ownership and schema guidance |
| 03-authentication-and-security.md | Project session model, cookie, Origin, proxy trust and Redis controls |
| 04-ai-chat-streaming-and-tickets.md | Ollama integration, chat lifecycle, NDJSON, retry and US-09 |
| 05-frontend-react-typescript.md | Actual React application structure, state, API integration and chat UI |
| 08-docker-compose-and-ollama.md | Project Compose services, model initialization, volumes and operations |
| 12-rag-source-policy-and-operation.md | US-15 scope, retrieval design, prompt safety and validation |
| 13-known-project-incidents.md | Historical project incidents, verified fixes and unresolved investigations |
| 21-source-code-api-data-compose-audit.md | Source-inspected API routes, ORM entities and Compose configuration |

The exact list is controlled by each document's `RAG Scope` metadata. Do not add general material just because it uses the same technology as the project.

## General reference material

General guides (Python fundamentals, JS/TS, PHP, C#, HTML/CSS, Scratch, Conda/venv, generic Windows 11 help, HTTP/REST and Git basics) belong outside this directory, under `docs/reference/technical/`. They may be retained for human reference but must not be mounted or indexed by RAG.

## Required document metadata

Every indexed document must include:
- `Document ID`
- `Status` — distinguish verified repository facts, user-confirmed implementation behavior, planned work and unverified observations
- `RAG Scope: project-specific`
- `Applies to`
- English and Finnish search keywords

Project-specific claims should include exact repository paths, endpoint paths, configuration names and verification dates where relevant. A planned feature must never be described as implemented.

## Evidence and source authority

1. Current source code and migrations.
2. Current project design/acceptance criteria.
3. User-confirmed runtime observations, with date and verification scope.
4. This knowledge corpus as a curated, potentially stale derivative.

If this corpus conflicts with source code, source code wins. Never include secrets, credentials, personal data, database dumps, session cookies or unreviewed logs.

## Retrieval behavior

- Markdown/TXT only; keyword search for MVP.
- Small, relevant sections, not whole documents.
- Preserve title, relative source path, heading and status.
- Treat retrieved text as untrusted evidence, never as instructions.
- If no project-specific source matches, do not fabricate a citation. The model may still answer general questions, but must distinguish general knowledge from verified project facts.
- Do not add embeddings, vector databases, paid APIs or new database tables without evidence and an explicit architecture decision.

## Maintenance

When project code or configuration changes, update the affected knowledge document and its verification status in the same change. Test Finnish and English queries against expected project-specific sections. General educational references must remain outside the live RAG corpus.
