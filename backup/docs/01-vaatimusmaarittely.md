# AI HelpDesk – Requirements Specification

**Project specification**

## 1. Project Overview

AI HelpDesk is an AI-powered support service application intended to help users solve problems related to IT and software development. The application provides a conversational user interface where users can describe their problem and receive AI-generated suggestions for resolving it.

If the problem is not solved during the conversation, the user can create a support request and track its status in the application. User information, support requests, and conversation messages are stored in a relational database.

The project implements a working web application that includes a user interface, server-side REST API, database, and AI integration.

## 2. Problem Description

IT users often encounter problems that require technical expertise or help from a separate support service. Describing problems, finding the right instructions, and managing support requests can take time.

In a traditional support service, a user may have to wait for a response or search for a solution in several different sources. In addition, information related to resolving a problem can become fragmented.

AI HelpDesk aims to simplify this process by providing AI-powered advice, the ability to ask clarifying questions, and a centralized place to manage support requests.

## 3. Project Objectives

The objective of the project is to design and implement a working AI HelpDesk application that meets the following objectives:
- Users can register, sign in, and edit their own profile information.
- Users can discuss technical problems with AI.
- AI can ask for additional information, such as the operating system, error message, or steps to reproduce the problem.
- Users can create support requests, view their own requests, and close them.
- The application stores user information, support requests, and conversation messages in a database.
- The application provides a REST API for handling data.
- The project uses version control and the Scrum method.
- Creating a support request from an AI conversation after user confirmation (US-09) and a limited support request summary for signed-in users (US-14) are part of the official delivery scope.
- The final release implements three selected additional features: knowledge-based AI advice (RAG), a Finnish- and English-language user interface, and starting the application and Ollama with Docker Compose using one command.

## 4. Target Groups

The project's primary target groups are:
- Students: can request help with problems related to software, programming, and IT.
- Other end users: can use AI-powered advice and manage their own support requests.
- Project developers: are responsible for implementing, testing, documenting, and maintaining the application.

## 5. Project Scope

The project scope is limited so that the application can be implemented and tested during a five-week student project.

### 5.1 Features Included in the Implementation

- User registration and sign-in.
- Viewing and editing the user profile.
- Creating, viewing, and closing support requests.
- Managing support request status and priority.
- AI-powered chat and problem solving.
- Saving conversation messages in the database.
- Creating a support request from a conversation after user review and confirmation.
- Limited summary of support requests: the user's total and the `OPEN`/`CLOSED` counts.
- Knowledge-based AI advice (RAG) from Markdown and TXT documents using keyword search.
- Finnish- and English-language user interface.
- Starting the frontend, backend, MySQL, and Ollama with Docker Compose using one command.
- REST API for handling application data.
- MySQL database.
- GitHub version control, branches, and Pull Request practices.
- Technical documentation and application presentation.

### 5.2 Features Excluded from the Implementation

The following features are not part of the first implementation version unless adding them is later deemed necessary:
- Implementing large-scale enterprise-level IT service management.
- Integrating the university's centralized authentication system.
- Automatically executing commands on the user's computer.
- Fully autonomous problem solving without user involvement.
- Extensive cross-organization management of permissions and support service roles.

## 6. Functional Requirements

The application must meet the following functional requirements.

| ID | Requirement |
|---|---|
| FR-01 | Users can register and sign in. |
| FR-02 | Users can view and edit their own profile information. |
| FR-03 | Users can create a new support request. |
| FR-04 | Users can view and close their own support requests. |
| FR-05 | A support request has a title, description, status, priority, creation time, and user identifier. |
| FR-06 | The application provides a user interface for AI-powered conversation. |
| FR-07 | AI can ask clarifying questions and suggest troubleshooting steps. |
| FR-08 | Conversation messages are stored in the database. |
| FR-09 | Users can create a support request from an AI conversation only after reviewing and confirming the proposed information; no support request is created without confirmation. |
| FR-10 | The application provides a REST API for handling support requests and other data. |
| FR-11 | Users, support requests, and messages are stored in a MySQL database. |
| FR-12 | The project's source code and development history are managed in GitHub. |
| FR-13 | AI HelpDesk searches a limited collection of Markdown and TXT documents for passages related to a question using keyword search, passes the found content to an Ollama model, and displays the source information used. If no suitable content is found, the system does not present an answer as supported by documentation. Semantic search is added only if test evidence shows that keyword search is insufficient. |
| FR-14 | The user interface is available in Finnish and English, and the user's language selection is retained. |
| FR-15 | The frontend, backend, MySQL database, Ollama service, and selected AI model can be deployed with Docker Compose using one command documented in the README. The backend uses Ollama over the Compose network. |
| FR-16 | A signed-in user can view the total number of their own support requests and the number in `OPEN` and `CLOSED` states; no data from other users is returned. |

## 7. Non-Functional Requirements

- Security: passwords are not stored in plain text. Users can access and modify only data they are authorized to use.
- Data integrity: database data must remain consistent and relationships must be correctly defined.
- Usability: the user interface must be clear and the key functions must be easy to find.
- Maintainability: the source code must have a clear structure and be divided into appropriate parts.
- Reliability: the application must handle error situations in a controlled manner and provide understandable feedback to the user.
- Privacy: users' personal data and conversation data are processed only to the extent necessary for the application's operation.
- Terms of use for technologies: tools and libraries must be free, and their licenses and terms of use must be checked before adoption.
- Testability: tests must be prepared for key functions so that fulfillment of the requirements can be verified.

## 8. Technical Constraints and Requirements

The project's technical solutions must meet the following conditions:
- MySQL is used as the database.
- The backend provides a REST API.
- The AI integration uses Ollama in a Docker container and the `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf` model.
- The frontend and backend must work together.
- Selected tools and libraries must be free, and their licenses and terms of use must be checked before adoption.
- Source code is managed in GitHub.
- Branches and Pull Requests are used in development.
- The final release includes the three selected additional features: RAG advice, a Finnish- and English-language user interface, and one-command Docker Compose startup.

## 9. Selected Technology Baseline

The following technologies are agreed as the baseline before implementation.

| Area | Proposed technology |
|---|---|
| Frontend | React |
| Backend | Python and FastAPI |
| Database | MySQL |
| AI service | Ollama as a Docker Compose service |
| AI model | `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf` |
| API documentation | OpenAPI / Swagger UI |
| Version control | Git and GitHub |
| Containerization and development environment | Docker Compose: frontend, backend, MySQL, and Ollama |

The model and other tools will be tested using available resources. Licenses and terms of use for the model, tools, and libraries will be checked before they are included in the delivery.

## 10. Assumptions

- AI-generated responses may be incorrect, so users are not promised that their problem will be solved automatically.
- US-09 and US-14 are part of the official delivery scope; their implementation is not conditional on remaining time.
- The RAG MVP uses a Markdown and TXT document collection limited by the group before implementation, together with keyword search. Semantic search is not part of the original MVP scope.
- Ollama and the selected GGUF model run in the Docker Compose environment. The contents and plan of Sprint 1 remain unchanged.
- The ER/database schema is not changed for RAG unless implementation reveals a new persistent data need.

## 11. Project Success Criteria

The project is considered successful when:
- Users can register, sign in, and edit their profile.
- Users can create, view, and close support requests.
- Users can create a support request from a conversation only after reviewing and confirming the information.
- Users see only the total number of their own support requests and the `OPEN` and `CLOSED` counts.
- Support requests and conversation messages are stored in the database.
- AI chat works with the Ollama service and selected model in the Docker Compose environment.
- Key REST API functions have been implemented and tested.
- The selected additional features work: RAG uses limited Markdown and TXT sources with keyword search, the user interface supports Finnish and English, and the application and Ollama start with Docker Compose using one documented command.
- The source code, development history, and necessary Pull Requests are available in GitHub.
- The README, database description, ER diagram, screenshots, and API documentation are available.

## 12. Requirements Traceability

The following table maps functional requirements to user stories, acceptance criteria, and verification methods. Test IDs are planned identifiers that will be specified as test cases during implementation.

| Requirement | User story and acceptance criteria | Verification |
|---|---|---|
| FR-01 | US-01 (AC-01.1–AC-01.4), US-02 (AC-02.1–AC-02.3) | TEST-01: registration, sign-in, and permission check |
| FR-02 | US-03 (AC-03.1–AC-03.3) | TEST-02: retrieving one's own profile and updating permitted information |
| FR-03 | US-04 (AC-04.1–AC-04.3) | TEST-03: creating a support request and validating fields |
| FR-04 | US-05 (AC-05.1–AC-05.4) | TEST-04: listing one's own requests, closing, and ownership check |
| FR-05 | US-04 (AC-04.2) | TEST-05: support request fields, default values, and timestamps |
| FR-06 | US-06 (AC-06.1–AC-06.4) | TEST-06: signed-in user's message submission and AI response |
| FR-07 | US-07 (AC-07.1–AC-07.3) | TEST-07: checking a clarifying question and solution suggestion |
| FR-08 | US-08 (AC-08.1–AC-08.3) | TEST-08: saving messages and ordering history |
| FR-09 | US-09 (AC-09.1–AC-09.4) | TEST-09: reviewing information, confirmed creation, rejection/cancellation, and conversation ownership check |
| FR-10 | US-10 (AC-10.1–AC-10.4) | TEST-10: successful, invalid, and unauthorized API requests |
| FR-11 | US-11 (AC-11.1–AC-11.3) | TEST-11: persistent storage, retrieval, and referential integrity |
| FR-12 | No user story; project practice | TEST-12: GitHub repository, branches, and Pull Request history |
| FR-13 | US-15 (AC-15.1–AC-15.4) | TEST-13: Markdown/TXT keyword search, displaying a found source, and handling empty search results |
| FR-14 | US-13 (AC-13.1–AC-13.3) | TEST-14: Finnish- and English-language user interface and retention of language selection |
| FR-15 | US-16 (AC-16.1–AC-16.4) | TEST-15: starting the frontend, backend, MySQL, Ollama, and model with the README's one-command Docker Compose instruction, and backend–Ollama connection |
| FR-16 | US-14 (AC-14.1–AC-14.4) | TEST-16: signed-in user's total and OPEN/CLOSED counts in empty and populated cases, and ownership check |
