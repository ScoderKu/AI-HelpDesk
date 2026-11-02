# AI HelpDesk – Sprint Plan (Scrum framework)

## 1. Purpose of the Sprint Plan

This document defines the preliminary Sprint Plan for the AI HelpDesk application. It describes Sprint goals, user stories to be implemented, workload estimates, key tasks, and expected outcomes.

Detailed descriptions and acceptance criteria for the user stories are in the document `02-käyttäjätarinat ja hyväksymiskriteerit.md`. Priorities and original Story Point estimates are defined in the document `03-product backlog.md`.

---

## 2. Sprint Overview

| Sprint | Goal | User stories | SP |
|-----------|----------|----------------|----|
| Sprint 1 | Technical foundation, user authentication, and Docker Compose | US-01, US-02, US-10, US-11, US-12, US-16 | 33 |
| Sprint 2 | Support request and profile management | US-03, US-04, US-05 | 13 |
| Sprint 3 | AI conversation and conversation history | US-06, US-07, US-08 | 18 |
| Sprint 4 | Completing the user experience | US-09, US-13, US-14 | 9 |
| Sprint 5 | Knowledge-based AI advice | US-15 | 13 |
| **Total** |  | **16 user stories** | **86 SP** |

Story Point totals are agreed planning estimates. Sprint 1 will remain a whole of 33 SP, and the current Sprint allocation will remain unchanged. US-09, US-14, RAG, and the other features selected for the final delivery scope are not conditional on time being available. If capacity risk materializes, it will be raised for a decision and changes will be approved through change management; commitments will not be silently removed.

---

# 3. Sprint 1 – Technical Foundation and User Authentication

## 3.1 Sprint Goal

Build the application's technical foundation, database connection, REST API structure, user authentication, and Docker Compose startup for the frontend, backend, MySQL, and Ollama.

At the end of the Sprint, the application will have a basic structure to which support request management and AI functions can later be connected.

## 3.2 Sprint Backlog

| ID | User story | SP |
|----|----------------|----|
| US-10 | Using the REST API | 8 |
| US-11 | Persistently storing data | 5 |
| US-01 | User registration | 5 |
| US-02 | User sign-in | 5 |
| US-12 | User interface usability | 5 |
| US-16 | Starting the application with Docker Compose | 5 |
| **Total** |  | **33** |

## 3.3 Key Development Tasks

1. Create the project frontend and backend structure.
2. Define the MySQL database structure and key tables.
3. Implement the database connection and basic data storage functions.
4. Implement the basic REST API structure and shared error responses.
5. Implement user registration and secure password storage.
6. Implement sign-in and permission checks for protected functions.
7. Create the basic user interface structure, navigation, and form components.
8. Create Docker configurations for the frontend, backend, and Ollama, and Compose services for those and the MySQL database.
9. Automatically deploy the selected GGUF model in the Ollama container using a `Modelfile`, and add persistent storage for the model and MySQL and readiness checks for services.
10. Add an example environment variable file and document `docker compose up --build`; test clean startup, model availability, and the backend's connections to MySQL and Ollama.
11. Test key registration, sign-in, database, and startup functions.

## 3.4 Expected Outcomes

1. The application frontend and backend work together.
2. Data can be stored in and retrieved from the database.
3. Users can register and sign in.
4. The basic REST API structure is available.
5. The key user interface views and navigation are in place.
6. The frontend, backend, MySQL, Ollama, and selected AI model are available after startup using the Docker Compose command documented in the README.

## 3.5 Sprint Acceptance

The Sprint can be accepted when the user stories selected for the Sprint Backlog and marked complete meet the acceptance criteria in the original `02-käyttäjätarinat ja hyväksymiskriteerit.md` document and the shared Definition of Done criteria.

---

# 4. Sprint 2 – Support Request and Profile Management

## 4.1 Sprint Goal

Enable users to manage their own profile information and support requests.

At the end of the Sprint, users can create a support request, view their own requests, and close a resolved request.

## 4.2 Sprint Backlog

| ID | User story | SP |
|----|----------------|----|
| US-04 | Creating a support request | 5 |
| US-05 | Viewing and closing one's own support requests | 5 |
| US-03 | Managing the user profile | 3 |
| US-17 | Administrator-assisted forgotten password reset (after US-04, US-05, and US-03) | 2 |
| **Total** |  | **15** |

## 4.3 Key Development Tasks

1. Implement retrieval and updating of profile information.
2. Implement the support request creation form and data validation.
3. Save the support request title, description, status, priority, creation time, and owner.
4. Implement a list view of the user's own support requests.
5. Implement viewing the details of an individual support request.
6. Implement closing a support request.
7. Ensure that users cannot view or modify another user's support request without authorization.
8. Test data storage, updates, retrieval, and permission checks.
9. Implement the protected backend maintenance command for US-17; generate a one-time temporary password, store only its hash, set the mandatory-change flag, and revoke all existing sessions in one transaction.
10. Enforce mandatory password change centrally in the backend so a temporary-password session can only change the password or sign out; test direct API access as well as the frontend flow.
11. Document the administrator's reset procedure and secure out-of-band delivery of the temporary password.

## 4.4 Expected Outcomes

1. Users can view and update their own profile information.
2. Users can create a support request.
3. Users can see their own support requests and their statuses.
4. Users can close their own open support request.
5. Support request permissions are checked in the backend.
6. An authorized operator can reset a forgotten password using the protected backend maintenance command; the temporary password is displayed only after a successful transaction.
7. Existing sessions are revoked, and the user must change the temporary password before using other protected features.
8. The administrator procedure and security precautions are documented.

## 4.5 Sprint Acceptance

The Sprint can be accepted when the acceptance criteria for US-04, US-05, and US-03 are met and support request storage, retrieval, and permissions work in tested situations. US-17 is accepted only after those three stories have been completed and checked, and its backend reset flow, forced password-change restriction, session revocation, and administrator instructions have passed their tests.

---

# 5. Sprint 3 – AI Conversation and Conversation History

## 5.1 Sprint Goal

Implement the key AI feature of the AI HelpDesk application. Users must be able to chat with AI, receive clarifying questions, and view their previous conversations.

## 5.2 Sprint Backlog

| ID | User story | SP |
|----|----------------|----|
| US-06 | AI-powered conversation | 8 |
| US-08 | Saving conversation messages | 5 |
| US-07 | Clarifying questions and problem solving | 5 |
| **Total** |  | **18** |

## 5.3 Key Development Tasks

1. Configure Ollama and the selected GGUF model running in the Docker Compose environment.
2. Implement the integration between the backend and the Ollama service over the Compose network.
3. Implement the conversation view and message submission.
4. Display AI responses in the user interface.
5. Pass the necessary conversation context in follow-up questions.
6. Implement the handling of clarifying questions and suggestions for resolving problems.
7. Save user messages and AI responses in the database.
8. Implement retrieval and display of previous conversations in the correct order.
9. Handle AI service errors and timeouts.
10. Test normal conversation behavior, follow-up questions, storage, and error situations.

## 5.4 Expected Outcomes

1. Users can send a message about a technical problem to the Ollama service running in Docker.
2. The AI response is displayed in the conversation view.
3. The conversation can continue based on previous context.
4. AI can request additional information needed to investigate the problem.
5. User and AI messages are saved in the database.
6. Users can view their saved conversations.

## 5.5 Sprint Acceptance

The Sprint can be accepted when sending conversations, displaying responses, and saving messages work according to the acceptance criteria. AI service errors must also be handled in a controlled manner.

---

# 6. Sprint 4 – Completing the User Experience

## 6.1 Sprint Goal

Extend the application's functionality and improve the user experience. Users can create a support request from a conversation, change the user interface language, and track a support request summary.

## 6.2 Sprint Backlog

| ID | User story | SP |
|----|----------------|----|
| US-09 | Creating a support request from a conversation | 3 |
| US-13 | Multilingual user interface | 3 |
| US-14 | Support request summary view | 3 |
| **Total** |  | **9** |

## 6.3 Key Development Tasks

1. Add the ability to create a support request based on a conversation.
2. Form the information needed for a support request draft from the conversation content.
3. Allow the user to review and confirm creation of the support request.
4. Implement Finnish- and English-language user interface text.
5. Implement language selection and retention of the selected language as agreed.
6. Implement a summary of the total number of support requests and their status breakdown.
7. Test the user interface, data, and error situations for the new functions.

## 6.4 Expected Outcomes

1. Users can move from an unresolved conversation to creating a support request, review and edit the proposed title and description, and confirm its creation.
2. A support request is not created without the user's explicit confirmation; rejection or cancellation does not create a request.
3. Users can switch the user interface between Finnish and English.
4. Users can view the total number of their own support requests and the `OPEN`/`CLOSED` counts; all counts are zero in an empty summary.

## 6.5 Sprint Acceptance

The Sprint can be accepted when the additional features meet their defined acceptance criteria and work together with the previously implemented functions.

---

# 7. Sprint 5 – Knowledge-Based AI Advice (RAG)

## 7.1 Sprint Goal

Extend AI advice so that technical documentation can be used in responses. The goal is to improve the relevance of responses and make it possible to connect responses to available sources.

## 7.2 Sprint Backlog

| ID | User story | SP |
|----|----------------|----|
| US-15 | Knowledge-based AI advice (RAG) | 13 |
| **Total** |  | **13** |

## 7.3 Key Development Tasks

1. Before implementation, limit the approved technical document collection to Markdown and TXT files.
2. Implement reading and processing files for keyword search.
3. Retrieve document passages matching the query keywords and their source information.
4. Define test questions and assess the relevance of keyword search and handling of empty results.
5. Pass the found content and actual source information to the Ollama model to generate a response.
6. Display source information in the user interface when available.
7. Handle situations where no suitable documentation is found.
8. Test the relevance of search results, response quality, and error situations.

## 7.4 Expected Outcomes

1. Technical documentation can be added to the system.
2. Content related to a user's question can be searched for in the documentation.
3. AI can generate a response based on the found content.
4. The actual source information for the found content is shown to the user.
5. When documentation is unavailable, the system does not present a response as supported by documentation.

## 7.5 Sprint Acceptance

The Sprint can be accepted when documentation search and AI integration work according to the defined acceptance criteria.

The RAG MVP search method is keyword search over Markdown and TXT files. Semantic search is not implemented by default; adding it requires documented evidence that keyword search does not meet the defined test criteria.

If the implementation proves too extensive for one Sprint, the user story is divided into smaller parts, such as documentation indexing, search implementation, and AI integration.

---

# 8. Shared Sprint Practices

## 8.1 Sprint Planning

Before the Sprint begins, the development team:

1. Reviews Product Backlog priorities and dependencies.
2. Selects user stories that match the Sprint goal.
3. Ensures the acceptance criteria are understandable.
4. Assesses the team's available capacity.
5. Divides user stories into smaller technical tasks as needed.

## 8.2 During the Sprint

1. Development work is tracked on the agreed task board.
2. Implementation progress and impediments are discussed regularly.
3. Code is tested and reviewed before merging into the main branch.
4. New requirements are added to the Product Backlog and prioritized separately.
5. The Sprint goal is not changed without a shared assessment of the change's impact.

## 8.3 Sprint Review

At the end of the Sprint, the implemented functions and their compliance with the acceptance criteria are reviewed.

1. Demonstrate a working software version.
2. Review user stories marked complete.
3. Collect feedback and identify necessary changes.
4. Update the Product Backlog based on findings.

## 8.4 Sprint Retrospective

At the end of the Sprint, the development team assesses:

1. What went well?
2. What problems slowed implementation?
3. How can collaboration and technical practices be improved?
4. What concrete improvement will be tried in the next Sprint?

---

# 9. Definition of Done

A user story can be marked complete when:

1. All acceptance criteria for the user story are met.
2. The implementation has been integrated into the application.
3. Input validation and error handling work.
4. Permissions and security have been taken into account.
5. The necessary unit and integration tests pass.
6. The user interface behavior has been checked.
7. Documentation has been updated as needed.
8. The implementation has been reviewed according to the agreed development process.

A Sprint is not automatically considered successful just because all planned Story Points have been addressed. The most important things are achieving the Sprint goal and delivering working, tested software.

---

# 10. Risks and Plan Refinement

| Risk | Impact | Mitigation |
|---------|----------|--------------------|
| Delay in the database or REST API | Implementation of other functions is delayed | Implement the technical foundation first and define APIs early |
| AI service errors or limitations | Conversation functionality does not work reliably | Test the integration early and implement error handling |
| Too much work in one Sprint | Some functionality remains unfinished | Divide stories into smaller parts and adjust the Sprint contents |
| Technical uncertainty in the RAG implementation | The final Sprint goal may be delayed | Conduct a technical investigation and limit the first implementation |
| Permission errors | User data may be exposed without authorization | Test backend permission checks and data ownership |

---

# 11. Summary

The preliminary Sprint Plan for the AI HelpDesk application consists of five Sprints and 16 user stories. The initial total estimate for the stories is **86 Story Points**, including the 5 Story Point estimate for US-16 allocated to Sprint 1.

1. Sprint 1 establishes the application's technical foundation.
2. Sprint 2 implements profile and support request management.
3. Sprint 3 introduces AI conversation and conversation history.
4. Sprint 4 completes the user experience and other Backlog functions.
5. Sprint 5 extends AI advice using technical documentation.

The plan is preliminary. The exact contents, duration, and workload of the Sprints will be confirmed based on developer capacity, technical dependencies, and project requirements.
