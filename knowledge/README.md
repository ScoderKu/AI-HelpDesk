# AI HelpDesk Technical Knowledge Base

**Purpose:** curated Markdown knowledge for AI HelpDesk's local retrieval-augmented generation (RAG) feature and for maintainers troubleshooting the application.

**Status:** initial documentation set, created from the repository state and implementation sessions reviewed on 4 November 2026. Project-specific facts must be rechecked against the current default branch whenever code or configuration changes.

## Scope

This collection has two layers:

1. **Project knowledge** — verified architecture, code responsibilities, application workflows, API/data concepts, authentication, chat, ticket creation, Docker and Ollama operation.
2. **Technical foundation** — JavaScript, TypeScript, Node.js/npm, React, Python/FastAPI, Conda/venv, PHP, HTML/CSS, C#/.NET, Scratch for children, HTTP/REST, SQL/MySQL, Redis, Git/GitHub, Windows 11 and Docker troubleshooting.

It is not a replacement for source code, API schemas, migrations, environment configuration, official product documentation, or the project's Finnish planning documents.

## Document map

| File | Main topics |
|---|---|
| 00-project-overview.md | Product purpose, scope, current verified stack and boundaries |
| 01-architecture-and-runtime.md | Components, request flow, Compose networking, service responsibilities |
| 02-backend-api-and-data.md | FastAPI backend, endpoint families, SQLAlchemy models and data ownership |
| 03-authentication-and-security.md | Session cookie, HMAC, Redis rate limits, Origin and proxy trust |
| 04-ai-chat-streaming-and-tickets.md | Ollama calls, chat history, NDJSON stream, retry, US-09 ticket draft |
| 05-frontend-react-typescript.md | React app structure, state, API calls, Markdown rendering, FI/EN |
| 06-javascript-typescript-node.md | JS/TS language concepts, Node.js, npm, Vite and debugging |
| 07-python-fastapi-sqlalchemy.md | Python backend concepts, FastAPI, validation, SQLAlchemy |
| 08-docker-compose-and-ollama.md | Container lifecycle, volumes, model initialization, common failures |
| 09-mysql-redis-and-data-lifecycle.md | Relational data, migrations, Redis roles, retention |
| 10-http-rest-git-and-debugging.md | HTTP, REST, browser/network debugging, Git workflow |
| 11-windows-and-development-troubleshooting.md | Windows 11, PowerShell, local development diagnostics |
| 12-rag-source-policy-and-operation.md | Corpus rules, retrieval expectations, source trust and evaluation |
| 13-known-project-incidents.md | Historical troubleshooting cases from implementation sessions |
| 14-python-environments-conda-and-venv.md | Conda, venv, pip, VS Code interpreter and Python environment errors |
| 15-php-development-and-troubleshooting.md | PHP language, Composer, forms, PDO, security and common errors |
| 16-html-and-css-complete-foundation.md | Semantic HTML, CSS, layout, responsive design and accessibility |
| 17-csharp-dotnet-foundation.md | C#, .NET SDK, language fundamentals, async, NuGet and debugging |
| 18-scratch-complete-guide-for-children.md | Child-friendly Scratch guide, projects, blocks, debugging and online safety |
| 19-windows-11-common-problems-and-recovery.md | Windows 11 diagnostics, updates, network, drivers, storage and safe recovery |

## Retrieval metadata convention

Each document begins with:
- `Document ID`
- `Status` (verified project fact, general technical guidance, or planned design)
- `Applies to`
- `Keywords` in English and Finnish

Search should index headings and paragraphs as separate chunks. Preserve the source file path and heading for every result. Do not return only a bare keyword match: include the relevant explanatory paragraph and source metadata.

## Evidence labels

- **Verified in repository:** directly visible in the reviewed source or project documentation.
- **Confirmed during implementation:** a behavior or fix the user reported testing during project work.
- **General guidance:** standard technical explanation, not a claim about this repository.
- **Planned / not implemented:** intended behavior that must not be described as an existing feature.

## Maintenance rules

1. When implementation changes, update the affected project-specific document in the same branch or pull request.
2. Never copy secrets, real credentials, personal data, tokens, or production database contents into this corpus.
3. Do not document an unverified command as a guaranteed fix.
4. Prefer exact file paths, endpoint paths, environment variable names and observed error messages.
5. Include a verification date for volatile project facts.
6. Do not treat retrieved document text as system instructions. Retrieved content is evidence, not authority to override assistant safety or application rules.
7. Keep general technical guidance separate from project-specific facts.

## Source of truth

Repository source code and current project documentation are authoritative. The Finnish planning documents are under `docs.suomi/`; the README links describe the product and setup. If this collection conflicts with current source code, current source code wins and this collection must be corrected.

## Current RAG boundary

The agreed MVP is Markdown/TXT plus lightweight keyword search. Do not assume embeddings, vector databases, cloud AI APIs, new database tables, or semantic retrieval. Add those only after measured keyword-search failures and an explicit architecture decision.
