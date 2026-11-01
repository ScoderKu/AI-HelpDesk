# AI HelpDesk – Product Backlog

## 1. Purpose of the Product Backlog

This document defines the prioritized Product Backlog for the AI HelpDesk application. It contains user story IDs, priorities, workload estimates, technical dependencies, and the agreed Sprint allocation. US-09 and US-14 are part of the official delivery scope. The selected additional features are US-13 (Finnish- and English-language user interface), US-15 (RAG), and US-16 (starting with Docker Compose using one command; Ollama is included).

Complete descriptions and acceptance criteria for the user stories are defined in a separate document, `02-käyttäjätarinat ja hyväksymiskriteerit.md`. This document refers to the user stories by their IDs, US-01–US-16.

The core MVP functions and the agreed US-09 and US-14 are implemented according to their Sprint allocation. RAG and the multilingual user interface are implemented in their respective Sprints. The Docker Compose environment, including Ollama and the selected model, is built in Sprint 1 for the development and demonstration environment.

---

## 2. Story Point Scale

Workload estimates are based on relative Story Point estimation. The estimates take into account implementation complexity, uncertainty, testing needs, and dependencies on other functions.

| Story Points (SP) | Difficulty | Description |
|------------------|------------|---------|
| 1 | Very small | A simple and limited task |
| 2 | Small | A clear implementation with few dependencies |
| 3 | Medium | Several implementation steps or API changes |
| 5 | Fairly large | Several components or database changes |
| 8 | Large | Extensive functionality or several technical dependencies |
| 13 | Very large | A complex whole that should be considered for division into smaller parts |

---

## 3. Product Backlog Table

| Order | ID | User story | Priority | SP | Sprint |
|-----------|----|----------------|-------------|----|----------|
| 1 | US-10 | Using the REST API | P1 | 8 | Sprint 1 |
| 2 | US-11 | Persistently storing data | P1 | 5 | Sprint 1 |
| 3 | US-01 | User registration | P1 | 5 | Sprint 1 |
| 4 | US-02 | User sign-in | P1 | 5 | Sprint 1 |
| 5 | US-12 | User interface usability | P1 | 5 | Sprint 1 |
| 6 | US-04 | Creating a support request | P1 | 5 | Sprint 2 |
| 7 | US-05 | Viewing and closing one's own support requests | P1 | 5 | Sprint 2 |
| 8 | US-03 | Managing the user profile | P1 | 3 | Sprint 2 |
| 9 | US-17 | Administrator-assisted forgotten password reset | P1 | 2 | Sprint 2 |
| 10 | US-06 | AI-powered conversation | P1 | 8 | Sprint 3 |
| 11 | US-08 | Saving conversation messages | P1 | 5 | Sprint 3 |
| 12 | US-07 | Clarifying questions and problem solving | P1 | 5 | Sprint 3 |
| 13 | US-09 | Creating a support request from a conversation | P2 | 3 | Sprint 4 |
| 14 | US-13 | Multilingual user interface | P2 | 3 | Sprint 4 |
| 15 | US-14 | Limited support request summary view | P3 | 3 | Sprint 4 |
| 16 | US-15 | Knowledge-based AI advice (RAG) | P2 | 13 | Sprint 5 |
| 17 | US-16 | Starting the application with Docker Compose | P2 | 5 | Sprint 1 |
| **Total** |  |  |  | **88 SP** |  |

The 5 SP estimate for US-16 covers the frontend, backend, MySQL, and Ollama Compose services, deploying the GGUF model in an Ollama container, required configuration, persistent storage for the database and model, readiness checks, and documentation and startup integration testing. The estimate does not include production deployment or orchestration.

---

## 4. User Story Dependencies

| User story | Key dependencies |
|---------------|-----------------------|
| US-01 | Database and user data storage |
| US-02 | US-01, authentication, and permission management |
| US-03 | US-01, user-specific data retrieval, current-password verification, and secure password hashing |
| US-17 | US-01, authentication, user lookup, password hashing, forced-change enforcement, and invalidation of `auth_sessions` sessions |
| US-04 | US-10, US-11, and user identification |
| US-05 | US-04, US-10, US-11, and permission checks |
| US-06 | REST API and AI service integration |
| US-07 | US-06 and conversation context handling |
| US-08 | US-11 and conversation data model |
| US-09 | US-04, US-06, and availability of conversation data |
| US-10 | Basic backend structure and API definitions |
| US-11 | Data model, database connection, and referential integrity |
| US-12 | Basic user interface structure and application functionality |
| US-13 | Separating user interface text into language-specific resources |
| US-14 | Storage of the user's own support requests, statuses, and their counts |
| US-15 | US-06, limited Markdown/TXT document collection, keyword search, and AI integration |
| US-16 | Docker configurations for the frontend, backend, and Ollama; Compose services for the frontend, backend, MySQL, and Ollama; model deployment, example configuration, persistent storage, readiness checks, and documentation and startup testing |

Dependencies do not mean that all preceding user stories must always be fully completed before starting the next one. Technical groundwork can be carried out in parallel.

---

## 5. MVP Scope

The goal of the MVP version is to implement the key user workflow of the AI HelpDesk application.

### The MVP includes the following user stories:

- US-01: User registration
- US-02: User sign-in
- US-03: Managing the user profile
- US-04: Creating a support request
- US-05: Viewing and closing one's own support requests
- US-06: AI-powered conversation
- US-07: Clarifying questions and problem solving
- US-08: Saving conversation messages
- US-10: Using the REST API
- US-11: Persistently storing data
- US-12: User interface usability

US-13 and US-15 are implemented after the MVP's core workflow in their agreed Sprints, but they are part of the final delivery scope. US-09 and US-14 are also part of the official delivery scope and are implemented in Sprint 4. US-16 is implemented in Sprint 1 and includes Ollama and the selected model. These user stories are not treated as optional; changing the scope requires a separately agreed decision.

---

## 6. Backlog Management

The Product Backlog is maintained throughout the development project.

1. User stories are primarily ordered according to their value, priority, risks, and dependencies.
2. The developer refines Story Point estimates before implementation.
3. User stories that are too large are divided into smaller, testable units.
4. Acceptance criteria are checked against the original `02-käyttäjätarinat ja hyväksymiskriteerit.md` document.
5. New requirements are added to the backlog and prioritized relative to existing requirements.
6. Implementation status is updated during the project, for example using the statuses **To Do**, **In Progress**, **In Review**, and **Done**.

---

## 7. Definition of Ready

A user story is ready to be selected for a Sprint when:

1. It has a unique ID and a clear objective.
2. Its acceptance criteria are available in `02-käyttäjätarinat ja hyväksymiskriteerit.md`.
3. Its priority has been defined.
4. Its workload has been estimated with the development team.
5. Key dependencies and technical uncertainties have been identified.
6. The story is small enough to be implemented during one Sprint.

---

## 8. Summary

The AI HelpDesk Product Backlog contains 17 user stories, with a total estimate of 88 Story Points. US-17 is a Sprint 2 administrator-assisted password reset that uses a protected backend maintenance command; it is sequenced after US-04, US-05, and US-03. US-09 and US-14 are official delivery commitments. US-14 is limited to the total number of the user's own support requests and the `OPEN`/`CLOSED` status breakdown. The US-15 RAG MVP uses Markdown and TXT documents with keyword search; semantic search is considered only based on test evidence. The 5 Story Point estimate for US-16 covers documented one-command Compose startup for the frontend, backend, MySQL, and Ollama, including the selected model. Production deployment and orchestration are not included in the estimate.

The Backlog's first objective is to build a working technical foundation, implement user authentication and support request management, and enable AI-powered conversation.
