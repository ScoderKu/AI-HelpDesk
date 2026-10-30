# AI HelpDesk – Project Management

> **Purpose of this document:** to serve as the project's shared governance document. This document describes the project's objectives, scope, schedule, responsibilities, risks, dependencies, monitoring, and change management. Detailed requirements, user stories, and implementation tasks are defined in the documents intended for them.

## 1. Project Details

| Information | Description |
|---|---|
| Project name | AI HelpDesk |
| Project type | Student project |
| Target project duration | 5 weeks |
| Planned workload | At least 20 hours per week, approximately 100 hours in total |
| Development model | Iterative work adapted from Scrum |
| Version control | Git and GitHub |
| Project owner | **Khoi Nguyen** |
| Key stakeholders | Project implementer, teacher, and application end users |
| Document status | Living document; updated as the project progresses |

**Current status on 26.10.2026:** the requirements specification, user stories with acceptance criteria, Product Backlog, Sprint Plan, system design, and UX/UI design have been aligned before implementation begins. The `backend` and `frontend` directories do not yet contain application source files. Implementation progress will henceforth be updated in the project tracking and GitHub tasks, not in this status snapshot.

## 2. Project Purpose and Objectives

AI HelpDesk is a web application that allows users to ask for help with IT and software development problems. Users can chat with AI, receive troubleshooting suggestions, and save an unresolved issue as a support request.

The project objectives are:

1. Implement a working web application with a user interface, backend, REST API, and relational database.
2. Allow users to register, sign in, and manage their own profile information.
3. Allow users to create, view, and close support requests, and save the information in a database.
4. Provide an AI-powered conversation in which users can describe their problem and receive suggestions for resolving it.
5. Save conversation messages and allow a support request to be created based on a conversation after the user has reviewed and confirmed it.
6. Implement a limited summary of support requests for signed-in users: the total number and the counts in `OPEN` and `CLOSED` states.
7. Implement the three selected additional features in the final release:
   - knowledge-based AI advice (RAG)
   - Finnish- and English-language user interface
   - starting the application and Ollama AI service with Docker Compose using one documented command.
8. Use GitHub version control and, where applicable, Scrum practices in the project.
9. Produce technical documentation, test results, and an application presentation.

Project success will be assessed based on the working software and acceptance criteria, as well as documentation, testing, version control, and the project presentation.

## 3. Project Scope

### 3.1 Included in the Project

The planned project scope includes:

- user registration and sign-in
- viewing and editing the user profile
- creating, viewing, and closing support requests
- saving support request status and priority
- AI-powered chat and clarifying questions
- saving conversation messages
- REST API
- MySQL database as specified in the current system design
- RAG-based advice using keyword search over a limited collection of Markdown and TXT documents; semantic search may be added only if test evidence shows that keyword search is insufficient
- Finnish- and English-language user interface text
- Docker Compose deployment for the frontend, backend, MySQL database, and Ollama AI service
- use of the local `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf` model in an Ollama container
- automated or repeatable tests for key functions
- README, API documentation, database description/ER diagram, screenshots, and presentation
- use of free tools and libraries, with their licenses and terms of use checked before selection and delivery.

### 3.2 Out of Scope

The following features are not included in the agreed core scope unless separately approved through change management:

- voice input or spoken responses
- creating PDF reports
- comprehensive enterprise-level IT service management
- integration with the university's centralized authentication
- automatically executing commands on the user's computer
- fully autonomous problem solving without user involvement
- extensive cross-organization permissions and integrations.

`US-09` and `US-14` are part of the official delivery scope. US-09 enables creating a support request from an AI conversation only after the user has reviewed and confirmed the proposed information. US-14 displays only the signed-in user's total number of support requests and the counts in `OPEN` and `CLOSED` states; it does not include charts, filtering, time comparisons, or other users' data. These are official user stories, not optional additional features.

The 5 Story Point estimate for `US-16` covers the frontend, backend, MySQL, and Ollama Compose services, deploying the selected model in an Ollama container, example configuration, persistent storage, readiness checks, and documentation and startup testing. Production deployment and orchestration are outside this scope. The contents of Sprint 1 and its 33 SP plan remain unchanged.

### 3.3 Scope Management Principle

The five-week timeframe and agreed delivery scope form the project's baseline. If the schedule or workload is at risk of being exceeded, the deviation will be recorded and its impact assessed against the project objectives and acceptance criteria. US-09, US-14, and the three selected additional features are official delivery commitments; they will not be removed or reduced silently. Any change requires an explicit decision in accordance with change management. The contents and plan of Sprint 1 will not be changed.

## 4. Roles and Responsibilities

The project is carried out as a student project. I perform several roles; naming the roles nevertheless helps keep responsibilities clear.

| Role | Responsibility |
|---|---|
| Project implementer / Developer | Designs, implements, tests, and documents the application, and maintains the GitHub repository. |
| Product Owner responsibility | Prioritizes the Product Backlog and proposes scope changes based on the project objectives. The student assumes this responsibility unless the teacher instructs otherwise. |
| Scrum Master responsibility | Plans weekly work, monitors impediments, and evaluates Sprint outcomes. The student applies these practices to their own work. |
| Testing responsibility | Creates and runs tests and records observed defects and test results. |
| Teacher | Assesses the work against the assignment and agreed assessment criteria and provides feedback as needed. The teacher is not assumed to be a day-to-day project decision-maker. |
| End user | Provides a perspective on the application's usability and needs; the user role is described in the requirements and user stories. |

Git branches and Pull Requests are used where possible to practice version control and the review process; the practices are kept lightweight for the size of the project.

## 5. Schedule and Milestones

The target project duration is five weeks. The M1–M5 milestones below are weekly target outcomes. The agreed division of the Product Backlog into five Sprints will be retained; the exact duration of the Sprints and their relationship to the weekly targets will be confirmed during Sprint Planning. User stories within the official delivery scope will not be silently removed due to capacity risk.

| Milestone | Timing | Key work | Evidence of completion |
|---|---|---|---|
| M1 – Planning and technical foundation | Week 1 | Reviewing requirements and backlog, refining architecture and data model decisions, repository practices, basic Docker Compose setup for Ollama and the selected model | Documented architecture decisions and a development environment with services that can be started, or a clearly documented technical blocker |
| M2 – Backend, database, and user management | Week 2 | Data model, database connection, basic REST API structure, registration and sign-in | Database works and key user management tests pass |
| M3 – Core support request workflow | Week 3 | Creating support requests, viewing and closing one's own requests, permission checks, technical foundation for conversations | A signed-in user can manage their own support requests |
| M4 – AI chat and user interface languages | Week 4 | Using the Ollama integration from the application, saving conversation messages, clarifying questions, Finnish- and English-language user interface; technical RAG trial | AI chat works in a controlled manner and language selection has been tested; the limited Markdown/TXT RAG source collection has been confirmed |
| M5 – RAG, integration, and delivery readiness | Week 5 | Keyword search over a limited document collection, checking the Docker Compose setup, regression testing, documentation, and demo | RAG, multilingual support, and Docker Compose with Ollama have been verified within the agreed scope; US-09 and US-14, README, API documentation, ER diagram, and demo are complete |

**Schedule clarification:** in the agreed allocation, `US-16` (Docker Compose, including Ollama and the selected model) is in Sprint 1, `US-09`, `US-13`, and `US-14` are in Sprint 4, and `US-15` (RAG with keyword search) is in Sprint 5. The RAG source collection and test questions can be prepared earlier. This Sprint allocation alone does not determine Sprint durations.

A Sprint goal is a plan, not a promise that every task will be completed at any cost. If workload estimates or technical impediments change, the Product Backlog and remaining goals will be reviewed.

## 6. Key Dependencies

| Item | Dependency | Management approach |
|---|---|---|
| User management | Data model, database connection, secure password handling, and authentication | Implement and test before expanding protected functionality |
| Support request management | REST API, database, and identification of the signed-in user | Test both owner permissions and prevention of unauthorized use |
| Saving conversation history | Data model for conversations and messages, and database connection | Define the relationships between messages and conversations during the architecture phase |
| AI chat | Backend connection to Ollama and the selected GGUF model running in the Docker Compose environment | Perform an integration trial early; test model loading, readiness, and service errors |
| RAG | AI chat, a Markdown/TXT source collection limited before implementation, and keyword search | Define test questions; test relevant matches, source details, and queries with no matches |
| Multilingual user interface | Separating user interface text into language resources | Agree how language selection is stored and test the key views in both languages |
| Docker Compose | Startup configuration, environment variables, persistent storage, and network connections for the frontend, backend, MySQL, Ollama, and model | Test the services and the backend's internal Ollama connection together; document one repeatable startup command |
| Final delivery | Test results, documentation, and working startup process | Reserve time in the final Sprint to review the whole application and fix missing items |

A dependency does not always mean that the entire preceding function must be complete before work on the next one can begin. For example, RAG source documents and the Docker structure can be prepared in parallel, provided that integrations are tested as a whole.

## 7. Risk Management

Risks are assessed qualitatively based on impact and likelihood. The register is updated at least at the end of each Sprint and whenever a significant new impediment arises.

| ID | Risk | Likelihood | Impact | Preventive action / contingency plan | Monitoring |
|---|---|---|---|---|---|
| R1 | Integrating the AI model or service takes longer than expected | Medium | High | Test the connection and one question-and-answer round early; keep the AI layer separate from the rest of the backend | Review during Sprint 1–2 |
| R2 | RAG keyword search does not find document passages relevant to the question | Medium | High | Use a limited Markdown and TXT collection; test with predefined questions and document the results; consider semantic search only based on test evidence | Review before RAG acceptance |
| R3 | The five-week workload is insufficient for all agreed features | Medium | High | Monitor progress weekly; raise deviations for a decision and formally agree on changes; do not automatically treat US-09 or US-14 as optional | Assess weekly |
| R4 | Docker services, Ollama model loading, or environment variables do not work together | Medium | High | Start the Compose structure in Sprint 1; test a clean startup, model availability, and the backend–Ollama connection; document configuration and secret handling | Review in each significant integration |
| R5 | A user can view or change another user's data | Medium | High | Check ownership in the backend; add unauthorized-use tests; do not rely solely on hiding things in the user interface | Test before delivery |
| R6 | Passwords or other secrets are handled insecurely | Low–medium | High | Store passwords only as securely hashed values; do not add credentials, API keys, or `.env` secrets to the repository | Review code and repository before the demo |
| R7 | User interface translations remain incomplete | Medium | Medium | Centralize text in language resources; test key views in Finnish and English | Review in Sprint 4 |
| R8 | Testing and documentation are left until the last minute | Medium | High | Record tests alongside implementation; reserve dedicated time in Sprint 5 for integration testing and documentation | Review during Sprint Review |
| R9 | The size, resource requirements, or license terms of the local GGUF model prevent a reliable demo | Medium | High | Test model loading and use in the project's Docker environment early; check the model and tools' licenses and terms of use before delivery | Review in Sprint 1 and before the presentation |
| R10 | The login IP limit identifies the Docker proxy instead of the actual client, or trusts incorrect forwarded address data | Medium | Medium | Assign the frontend proxy a fixed IP on a separate Compose network; read `X-Forwarded-For` only from a trusted proxy and select the first untrusted address from the right; also test forged and malformed headers | Unit tests passed; verify with real LAN clients before LAN deployment |

### 7.1 Procedure When a Risk Materializes

When a risk materializes:

1. record the issue and its impact in a GitHub Issue or project tracking
2. assess the impact on the Sprint goal, scope, and schedule
3. select a corrective action or limit the functionality
4. update the risk register and, if necessary, the change log
5. test the fix and record the result.

## 8. Progress Monitoring

### 8.1 Work Statuses

Work is tracked using the Product Backlog and GitHub Issues. The following statuses are used:

- **To Do** – work has not started
- **In Progress** – work is underway
- **In Review** – implementation is awaiting review or test review
- **Done** – acceptance criteria are met and the necessary documentation has been updated.

A task is not marked complete merely because the code has been written. Completion requires that the function has been implemented, tested against the acceptance criteria, and that known gaps have been recorded.

### 8.2 Weekly Monitoring Rhythm

At the beginning of each week:

1. review the Sprint goal and available time
2. select the most important tasks from the Product Backlog
3. ensure task dependencies and acceptance criteria are clear.

During each work session:

- update task statuses
- record significant technical problems and decisions
- make small, understandable Git commits
- keep unfinished changes on separate branches where possible.

At the end of each week:

1. compare completed outcomes with the Sprint goal
2. run the most important functional tests
3. record unfinished tasks and their reasons
4. assess risks and the workload for the following week
5. write a brief retrospective: what went well, what impeded progress, and what will be changed.

### 8.3 Progress Reporting

Progress is described primarily through verifiable outcomes, not merely a percentage. Examples:

- registration and sign-in pass the specified tests
- a user can create and close their own support request
- a conversation message is saved in the database
- a RAG response displays the source used or reports that no suitable source was found
- key user interface views work in Finnish and English
- the frontend, backend, database, and Ollama start with the documented Docker Compose command, and the backend receives a response from Ollama
- the README, API documentation, and ER diagram reflect the implemented system.

**Status on 31.10.2026:** Proxy handling for the login IP rate limit has been clarified. The frontend has a fixed address on a dedicated Docker proxy network, and the backend processes the `X-Forwarded-For` chain only when the peer is trusted. Six backend unit tests cover trusted and untrusted peers, single and chained proxy hops, distinct client addresses, and malformed or missing headers. The tests and Compose configuration validation passed. Forwarding between two actual LAN devices has not yet been tested and must be verified before LAN use. The current Compose port binding remains `127.0.0.1`, so this configuration is not accessible from other LAN devices.

### 8.4 Definition of Done

A user story or function can be marked complete when:

- its acceptance criteria are met
- the function has been appropriately tested
- error situations are handled reasonably
- security and permissions have been considered according to the scope of the function
- the code has been saved to GitHub and, where necessary, reviewed in a Pull Request
- related documentation has been updated
- known limitations have been recorded.

## 9. Change Management

Changes may include, for example, a new feature, a change to a requirement, a technology change, a change to the Sprint allocation, or refinement of an acceptance criterion.

### 9.1 Change Process

1. **Proposal:** record the need for and rationale behind the change in a GitHub Issue or change log.
2. **Impact assessment:** assess the effect on objectives, scope, workload, dependencies, security, and schedule.
3. **Prioritization:** compare the change with the current P1/P2/P3 tasks and mandatory requirements.
4. **Decision:** the project implementer decides on minor internal implementation changes. Changes affecting scope or assessment requirements are aligned with the teacher's instructions as needed.
5. **Update:** update the approved change in the appropriate source document, Product Backlog, and test plan as needed.
6. **Implementation and review:** implement and test the change, and mark its completion in project tracking.

### 9.2 Change Principles

- Requirement changes are primarily recorded in the requirements specification.
- Changes concerning user needs and acceptance criteria are recorded in the user story document.
- Work priorities, estimates, and Sprint allocation are maintained in the Product Backlog.
- This document is updated when a change affects project scope, schedule, significant risks, or governance practices.
- The README serves as the project's introduction, installation, configuration, and user guide. It may briefly describe the application's purpose, key features, and technologies; detailed requirements, Sprint tracking, risks, decisions, and the change log are kept in their own documents.

## 10. Decision Log

Significant technical and project management decisions are recorded in this table. Detailed implementation decisions may also be recorded in GitHub Issues.

| ID | Date | Decision | Rationale | Impact |
|---|---|---|---|---|
| D-01 | 26.10.2026 | The project duration is set to five weeks, with a workload of at least 20 hours per week | Project schedule and available working time | Scope must remain limited and priorities clear |
| D-02 | 26.10.2026 | RAG, a Finnish- and English-language user interface, and Docker Compose are selected for the final release | Additional features in the assignment and the project's learning objectives | These three features are planned and tested separately |
| D-03 | 26.10.2026 | US-09 and US-14 are part of the official delivery scope; US-14 includes only the user's total and OPEN/CLOSED counts | Final scope confirmed by the group | The stories are not treated as optional; US-09 requires user review and confirmation |
| D-04 | 26.10.2026 | US-16 includes Ollama and the selected GGUF model in the Docker Compose environment; Sprint 1 and its 33 SP plan remain unchanged | Containerization approach and Sprint decision confirmed by the group | The backend uses Ollama over the Compose network; production deployment is out of scope |
| D-05 | 26.10.2026 | The target AI model is `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`, used through Ollama | The project's selected local model | The model is started in an Ollama container; the model file location and persistent model storage are documented |
| D-06 | 26.10.2026 | The RAG MVP processes Markdown and TXT documents using keyword search; semantic search is added only based on test evidence | A limited and testable MVP implementation | The source collection is limited before implementation; the ER schema is not changed without a new persistent data need |
| D-07 | 26.10.2026 | Tools and libraries must be free, and their licenses and terms of use are checked | Technology decision confirmed by the group | Choices and possible limitations are documented before delivery |
| D-08 | 31.10.2026 | The backend trusts only the frontend proxy defined on the Compose network and uses the first untrusted hop in the trusted proxy's forwarded address chain as the login IP-rate-limit key | Prevent shared-proxy IPs from cross-limiting users and prevent misuse of forwarded headers | The frontend address is `172.30.0.2`, the trusted network is configured through `TRUSTED_PROXY_IPS`, and the logic is tested automatically; actual LAN forwarding will be verified later |

## 11. Change Log

| Date | Version | Change | Author |
|---|---|---|---|
| 26.10.2026 | 0.1 | First version of the project management document | Project implementer |
| 26.10.2026 | 0.2 | Updated current status, clarified the Sprint schedule and the scope of US-14 and US-16; clarified the responsibilities of the README and governance document | Project implementer |
| 26.10.2026 | 0.3 | Aligned the official scope, RAG MVP, Ollama and selected model, Docker Compose, license term checks, and US-09/US-14 commitments | Project implementer |
| 31.10.2026 | 0.4 | Documented the proxy-based login IP rate-limit change, test results, and outstanding LAN verification | Project implementer |

## 12. Links to Other Project Documents

- [Requirements Specification](01-vaatimusmaarittely.md)
- [User Stories and Acceptance Criteria](02-käyttäjätarinat%20ja%20hyväksymiskriteerit.md)
- [Product Backlog](03-product%20backlog.md)
- [Sprint Plan](04-sprintin%20suunnitelma.md)
- [System Design](05-järjestelmän%20suunnittelu.md)
- [README](../README.md)

> **Maintenance practice:** update this document as the project progresses, especially regarding the schedule, risks, significant decisions, and scope changes. Do not copy detailed requirements or user stories from other documents here; link to their sources.
