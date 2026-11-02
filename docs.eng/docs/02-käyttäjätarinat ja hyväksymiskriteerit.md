# AI HelpDesk – User Stories and Acceptance Criteria

## 1. User Roles

### 1.1 Registered User

A registered user can log in to the application, manage their own profile, chat with the AI, and create and manage their own support tickets.

### 1.2 Application Developer

The application developer is responsible for the application's technical implementation, database, REST API, AI integration, testing, and documentation.

## 2. User Stories and Acceptance Criteria

### US-01: User Registration

- As a student
- I want to register for the AI HelpDesk application.
- So that I can use the service's features with my own user account.

**Acceptance Criteria**

**AC-01.1 – Successful Registration**

- Given that the user does not yet have a user account.
- When the user provides a first name, last name, username, email address, and password in a valid format and submits the form.
- Then the system creates a user account and saves the user's information to the database.
- The password is hashed on the server side; the client cannot submit a `password_hash` value to be stored.

**AC-01.2 – Invalid Information**

- Given that the user is on the registration form.
- When any required information is missing or invalid.
- Then the system displays an error message and does not create a user account.

**AC-01.3 – Email Address Already in Use**

- Given that the email address already belongs to an existing user account.
- When the user attempts to register with the same email address.
- Then the system prevents a new account from being created and displays an error message.

**AC-01.4 – Password Security**

- Given that the user's registration is successful.
- When the password is saved to the database.
- Then the password is stored securely as a hash, not in plain text.

### US-02: User Login

- As a registered user
- I want to log in to the application.
- So that I can use my own information and the application's protected features.

**Acceptance Criteria**

**AC-02.1 – Successful Login**

- Given that the user has a valid user account.
- When the user provides the correct email address and password.
- Then the system allows the user to log in and opens the application's protected features.

**AC-02.2 – Invalid Login Credentials**

- Given that the user attempts to log in to the application.
- When the email address or password is invalid.
- Then the system prevents the login and displays an error message.

**AC-02.3 – Access to Protected Features**

- Given that the user is not logged in.
- When the user attempts to use a feature that requires login.
- Then the system prevents access to that feature.

### US-03: Managing the User Profile

- As a registered user
- I want to view and edit my own profile information.
- So that my information stays up to date.

**Acceptance Criteria**

**AC-03.1 – Viewing the Profile**

- Given that the user is logged in.
- When the user opens the profile page.
- Then the system displays the user's own profile information.

**AC-03.2 – Updating the Profile**

- Given that the user has opened their profile page.
- When the user edits their first name, last name, or username and saves the changes.
- Then the system saves the changes to the database and displays the updated information.
- In the MVP, the email address and password are not changed when updating the profile. Any possible changes to them require a separate, verified action.

**AC-03.3 – Invalid Profile Information**

- Given that the user edits their profile information.
- When the user enters invalid information.
- Then the system displays an error message and does not save the invalid changes.

### US-04: Creating a Support Ticket

- As a registered user
- I want to create a new support ticket.
- So that I can record my technical problem and track its handling.

**Acceptance Criteria**

**AC-04.1 – Creating a Support Ticket**

- Given that the user is logged in.
- When the user provides a support ticket title and description and submits the form; priority may be provided or omitted.
- Then the system creates a support ticket and saves it to the database.
- The backend sets the owner based on the authenticated user, sets the status to `OPEN`, and defaults a missing priority to `MEDIUM`; the client cannot set the owner or initial status.

**AC-04.2 – Support Ticket Basic Information**

- Given that the user creates a new support ticket.
- When the support ticket is successfully saved.
- Then the system saves the title, description, status, priority, creation time, and ticket owner.
- A ticket created from a conversation also stores the source conversation ID; for a ticket created independently, the source conversation is empty.

**AC-04.3 – Required Information Missing**

- Given that the user is opening a new support ticket.
- When the title or description is missing.
- Then the system reports the missing information and does not create the support ticket.

### US-05: Viewing and Closing Own Support Tickets

- As a registered user
- I want to view my own support tickets and close resolved tickets.
- So that I can track and manage the handling of my own issues.

**Acceptance Criteria**

**AC-05.1 – Support Ticket List**

- Given that the user is logged in and has saved support tickets.
- When the user opens the support ticket view.
- Then the system displays the user's own support tickets.

**AC-05.2 – Support Ticket Details**

- Given that the user is viewing their own support tickets.
- When the user opens an individual support ticket.
- Then the system displays the ticket's title, description, status, priority, and creation time.

**AC-05.3 – Closing a Support Ticket**

- Given that the user owns an open support ticket.
- When the user selects the option to close the support ticket.
- Then the system changes the ticket status to closed and saves the change.
- Closing is a separate action; the user cannot change the status directly through a general support ticket update request.

**AC-05.4 – Checking Permissions**

- Given that the support ticket belongs to another user.
- When the user attempts to view or modify that support ticket.
- Then the system prevents the unauthorized action.

### US-06: AI-Powered Conversation

- As a user working on a technical problem
- I want to discuss my problem with the AI.
- So that I can get suggestions for solving the problem.

**Acceptance Criteria**

**AC-06.1 – Sending a Message**

- Given that the user is logged in and has opened their own AI HelpDesk conversation.
- When the user writes about their problem and sends the message.
- Then the system forwards the message to the AI model or service in use.

**AC-06.2 – AI Response**

- Given that the AI service successfully receives the user's message.
- When the AI generates a response.
- Then the system displays the response in the conversation interface.

**AC-06.3 – AI Service Failure**

- Given that the user sends a message to the AI.
- When the AI service is unavailable or the request fails.
- Then the system displays an understandable error message.

**AC-06.4 – Continuing a Conversation**

- Given that the user has received an AI response.
- When the user sends a new message in the same conversation.
- Then the system forwards the necessary conversation context to the AI and displays the new response.

### US-07: Clarifying Questions and Problem Solving

- As a user investigating a technical problem
- I want the AI to ask clarifying questions when necessary.
- So that I can provide the information needed to solve the problem and receive more suitable instructions.

**Acceptance Criteria**

**AC-07.1 – Asking a Clarifying Question**

- Given that the user's problem description does not contain enough information.
- When the AI needs additional information to understand the problem.
- Then the AI asks a clarifying question relevant to the situation.

**AC-07.2 – Identifying the Technical Environment**

- Given that solving the problem depends on the operating system, software version, or error message.
- When the AI needs this information.
- Then the AI asks the user to provide the necessary additional information.

**AC-07.3 – Providing Suggested Solutions**

- Given that the user has provided the information needed to investigate the problem.
- When the AI generates a response.
- Then the system displays suggested solutions and next steps related to the problem.

### US-08: Saving Conversation Messages

- As a registered user
- I want to save my conversation messages to the database.
- So that I can view my previous conversations later.

**Acceptance Criteria**

**AC-08.1 – Saving the User's Message**

- Given that a logged-in user sends a message in their own conversation.
- When the message is accepted for saving.
- Then the system saves the message to the database and associates it with the correct conversation and user.

**AC-08.2 – Saving the AI Response**

- Given that the AI has generated a response to the user's message.
- When the response is processed successfully.
- Then the system saves the response to the database.

**AC-08.3 – Viewing a Previous Conversation**

- Given that the user has saved conversation messages.
- When the user opens a previous conversation.
- Then the system displays the saved messages in the correct order.
- The user cannot view another user's conversations or messages.

### US-09: Creating a Support Ticket from a Conversation

- As a user using an AI HelpDesk conversation
- I want to create a support ticket based on the conversation.
- So that I can preserve the problem information for further handling.

**Acceptance Criteria**

**AC-09.1 – Suggesting Support Ticket Creation**

- Given that the user's problem is not resolved during the conversation.
- When the problem needs further handling and the user is logged in.
- Then the system offers the user the option to create a support ticket.

**AC-09.2 – Review and Confirmed Creation**

- Given that the user selects the option to create a support ticket from the conversation.
- When the system opens a suggested title and description based on the conversation and the user can review or edit them and confirm creation.
- Then the system creates a support ticket and saves it to the database.
- The support ticket is linked to the conversation only if the conversation belongs to the same logged-in user.

**AC-09.3 – Respecting the User's Decision**

- Given that the system suggests creating a support ticket.
- When the user rejects the suggestion.
- Then the system does not create a support ticket automatically.

**AC-09.4 – Cancelling Creation**

- Given that the user reviews or edits the suggested support ticket information.
- When the user cancels creation or leaves without confirming it.
- Then the system does not save the support ticket.

### US-10: Using the REST API

- As an application developer
- I want to handle support tickets through the REST API.
- So that the frontend and backend can exchange information in a controlled manner.

**Acceptance Criteria**

**AC-10.1 – Retrieving Support Tickets**

- Given that the user is logged in and has the right to view their own support tickets.
- When the frontend sends a request to retrieve support tickets.
- Then the API returns the user's own support tickets.

**AC-10.2 – Creating a Support Ticket**

- Given that the user is logged in and the request contains valid information.
- When the frontend sends a support ticket creation request.
- Then the backend validates the information, saves the support ticket, and returns an appropriate response.

**AC-10.3 – Updating a Support Ticket**

- Given that the user has the right to modify the support ticket in question.
- When the frontend sends an allowed update request.
- Then the backend checks permissions and information before saving the change.

**AC-10.4 – Invalid or Unauthorized Requests**

- Given that the API receives an invalid or unauthorized request.
- When the backend processes the request.
- Then the API returns an appropriate HTTP error code and error response.

### US-11: Persistent Data Storage

- As an application user
- I want my user information, support tickets, and conversation messages to be stored persistently.
- So that I can continue using the application without losing saved information.

**Acceptance Criteria**

**AC-11.1 – Saving Data**

- Given that the user creates a support ticket or sends a conversation message to be saved.
- When the backend successfully processes the save request.
- Then the information is saved to the MySQL database.

**AC-11.2 – Retrieving Saved Data**

- Given that information has been saved to the database.
- When the application retrieves that information again.
- Then the system returns the correct information in accordance with permissions.

**AC-11.3 – Relationships Between Data**

- Given that the database contains users, support tickets, and messages.
- When data is saved and associated with one another.
- Then the database keys and referential integrity ensure the correct relationships between the data.

### US-12: Usability of the User Interface

- As an application user
- I want to use a clear and consistent user interface.
- So that I can easily find the features I need and understand the notifications provided by the application.

**Acceptance Criteria**

**AC-12.1 – Finding Key Features**

- Given that the user is logged in to the application.
- When the user opens the application's main view.
- Then they can find links to the conversation, support tickets, and profile.

**AC-12.2 – Feedback on Actions**

- Given that the user performs an action in the application.
- When the action succeeds or fails.
- Then the user interface displays appropriate feedback.

**AC-12.3 – Form Validation**

- Given that the user is filling in an application form.
- When required information is missing or invalid.
- Then the user interface explains what information the user needs to correct.

## 3. Selected Additional Features

US-09 and US-14 are part of the official delivery scope and will be implemented in Sprint 4 in accordance with their acceptance criteria. In addition, three additional features have been selected for the final release: US-13 (Finnish- and English-language user interface), US-15 (RAG), and US-16 (Docker Compose for the frontend, backend, MySQL, and Ollama, including the selected model). US-13 and US-15 will be implemented after the basic MVP in the agreed Sprint periods; they, US-09, and US-14 are not optional. The Docker Compose environment will be set up in Sprint 1.

### US-17: Administrator-Assisted Forgotten Password Reset

- As an authorized application administrator
- I want to reset a user's forgotten password using a backend maintenance command.
- So that the user can regain access without a public password-reset endpoint, email delivery, or OTP workflow.

**Acceptance Criteria**

**AC-17.1 – Backend-Only Administrative Reset**
- Given that a user cannot sign in because they have forgotten their password.
- When an authorized administrator runs the maintenance command in the protected backend environment for an existing user.
- Then the backend generates a temporary password and displays it only in the administrator's command output after the database transaction succeeds.
- There is no public password-reset endpoint or user-facing reset interface.

**AC-17.2 – Secure Temporary Password Handling**
- Given that the administrator initiates a password reset.
- When the backend generates the temporary password.
- Then it is generated using a cryptographically secure random number generator, shown only once, and only its password hash is stored in the database.
- The plaintext password and its hash are never written to application logs.

**AC-17.3 – Mandatory Password Change**
- Given that the user's password has been reset.
- When the user signs in with the temporary password.
- Then the system requires the user to change the password before allowing access to any other protected feature.
- The new password is validated and saved through the password-change operation.

**AC-17.4 – Revoke Existing Sessions**
- Given that the user may have active login sessions.
- When the administrator resets the password.
- Then the backend invalidates all existing sessions belonging to that user.

**AC-17.5 – Invalid Target or Unauthorized Execution**
- Given that the command is run for an unknown user or by a person without backend maintenance access.
- When the backend processes the command.
- Then the reset is aborted safely, no account data is changed, and no password or unnecessary account information is disclosed.

### US-13: Multilingual User Interface

- As an application user
- I want to switch the user interface language between Finnish and English.
- So that I can use the application in the language that suits me.

**Acceptance Criteria**

**AC-13.1 – Changing the Language**

- Given that the user opens the application.
- When the user selects Finnish or English.
- Then the user interface displays text in the selected language.

**AC-13.2 – Retaining the Selected Language**

- Given that the user has selected the user interface language.
- When the user moves to another view in the application.
- Then the selection persists in the browser from one view to another and the next time the user logs in.

**AC-13.3 – Coverage of User Interface Translations**

- Given that the user has selected Finnish or English.
- When the user uses the application's supported views and features.
- Then the user interface text and user-facing notifications are in the selected language.

The language selection applies to the user interface. The AI response language is determined by the conversation language and the agent's language instructions.

### US-14: Support Ticket Summary View

- As a user managing support tickets
- I want to see a summary of my own support tickets.
- So that I can track their number and statuses in one view.

**Acceptance Criteria**

**AC-14.1 – Displaying the Summary**

- Given that the logged-in user has saved support tickets.
- When the user opens the summary view.
- Then the system displays only the total number of the user's own support tickets and the numbers of tickets in `OPEN` and `CLOSED` status.

**AC-14.2 – Empty Summary**

- Given that the logged-in user has no support tickets.
- When the user opens the summary view.
- Then the system displays zero for the total and for the number of tickets in both statuses.

**AC-14.3 – Updating the Summary**

- Given that the user creates or closes one of their own support tickets.
- When the summary view data is updated.
- Then the total and status-specific numbers match the user's saved support tickets.

**AC-14.4 – Consistency and Ownership of Counts**

- Given that the logged-in user and other users have support tickets.
- When the user opens the summary view.
- Then the summary includes only the logged-in user's tickets, and the total equals the sum of the `OPEN` and `CLOSED` counts.

US-14 is part of the official delivery scope. The summary is limited to counts. It does not include charts, filters, time-period comparisons, or other users' support tickets. The MVP statuses are `OPEN` and `CLOSED`.

### US-15: Knowledge-Based AI Assistance (RAG)

- As a user investigating a technical problem
- I want the AI to use technical documentation in its responses.
- So that I can receive documentation-based and more targeted instructions.

**Acceptance Criteria**

**AC-15.1 – Searching Documentation**

- Given that a Markdown or TXT document containing a known keyword has been added to the limited source collection.
- When the user asks a question related to that document section.
- Then the system retrieves a matching content excerpt using keyword search, forwards it to the Ollama model, and retains the excerpt's source information for display.

**AC-15.2 – No Suitable Documentation Found**

- Given that keyword search does not find a suitable passage for the question in the limited document collection.
- When the AI generates a response.
- Then the system does not claim that the response is supported by found documentation.

**AC-15.3 – Displaying Sources**

- Given that documentation related to the query is found.
- When the system displays the AI-generated response.
- Then the user interface also displays the available source information.

**AC-15.4 – Supported Formats and Search Method**

- Given that a supported Markdown or TXT file has been added to the system.
- When the documentation is processed for search.
- Then the system can search its text content by keywords. The MVP does not use semantic search.

The exact collection of source documents for the RAG MVP will be defined before implementation. Semantic search may be proposed later only if test evidence collected using predefined questions shows keyword search to be insufficient.

### US-16: Starting the Application with Docker Compose

- As an application developer or administrator
- I want to start the application with one documented Docker Compose command.
- So that the development and demonstration environment can be brought up reproducibly.

**Acceptance Criteria**

**AC-16.1 – Starting with One Command**

- Given that Docker and Docker Compose are available and the required environment variables are set.
- When the user runs the startup command documented in the README.
- Then the frontend, backend, MySQL, and Ollama start without separate manual service startup steps, and the selected AI model is automatically imported into Ollama's model store if it is not already there.

**AC-16.2 – Service Readiness**

- Given that Docker Compose startup has been performed.
- When the services are ready to receive requests.
- Then the frontend can use the backend, the backend can use the MySQL database and Ollama service through the Compose network, and Ollama can load the selected model.

**AC-16.3 – Configuration and Secrets**

- Given that configuration values or secrets are required to start the application.
- When the developer prepares the local environment.
- Then the README and example configuration specify the required values, the location of the model source file, and the startup prerequisites, and the repository does not contain real secrets.

**AC-16.4 – Model Persistence and Restart**

- Given that Docker Compose has started the services and Ollama has loaded the selected model.
- When the Compose services are restarted without removing persistent storage.
- Then making the model available again does not require the user to perform a separate manual model download step.

The scope of US-16 includes Docker configurations for the frontend, backend, and Ollama; Compose services for the frontend, backend, MySQL, and Ollama; automatic initial setup of the selected GGUF model using the `Modelfile`; an example file containing the necessary environment variables but no real secrets; persistent storage for MySQL and the model store; service health checks; and documenting and testing the startup command. The one-command example is `docker compose up --build`. Production deployment and orchestration are outside the scope of the story.

## 4. Priority Table

| Priority | Description | Implementation Principle |
|---|---|---|
| P1 – High | Functionality essential to meeting the project's mandatory requirements | Implement first |
| P2 – Medium | Important functionality that complements application use | Implement after P1 functionality |
| P3 – Low | Functionality of lower value than other stories | Priority guides the order; a story selected for the official delivery scope will not be omitted without a separately approved scope change |

**Initial Priorities of User Stories**

| User Story | Priority |
|---|---|
| US-01: User Registration | P1 |
| US-02: User Login | P1 |
| US-03: Managing the User Profile | P1 |
| US-04: Creating a Support Ticket | P1 |
| US-05: Viewing and Closing Own Support Tickets | P1 |
| US-06: AI-Powered Conversation | P1 |
| US-07: Clarifying Questions and Problem Solving | P1 |
| US-08: Saving Conversation Messages | P1 |
| US-09: Creating a Support Ticket from a Conversation | P2 |
| US-10: Using the REST API | P1 |
| US-11: Persistent Data Storage | P1 |
| US-12: Usability of the User Interface | P1 |
| US-13: Multilingual User Interface | P2 – selected additional feature |
| US-14: Support Ticket Summary View | P3 – limited functionality included in the official delivery scope |
| US-15: Knowledge-Based AI Assistance (RAG) | P2 – selected additional feature |
| US-16: Starting the Application with Docker Compose | P2 – selected additional feature |

## 5. Summary

This document defines the AI HelpDesk application's user stories, acceptance criteria, and a separate priority table.

The user stories and acceptance criteria have been linked to the Product Backlog and the agreed Sprint plan. As implementation and testing progress, fulfilment of the acceptance criteria will be verified in accordance with the traceability table.
