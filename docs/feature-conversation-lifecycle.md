# Conversation Lifecycle — Implementation Specification

**Status:** Approved implementation scope; technical details are subject to source-code and runtime verification.
**Base:** `main` at `f2b8432f7e3f6545b1c63c259cf52c1feea349ea`
**Integration branch:** `feature/conversation-lifecycle`

## Goals and delivery order

Implement these three features sequentially on this integration branch:

1. Stop generation and supplement unanswered user input.
2. Context usage monitor.
3. New conversations with persistent context summaries, model-generated titles, and parent/child conversation navigation.

Do not merge to `main` without explicit user approval. Keep database migrations linear and owned by this integration branch. Run task-level tests before starting the next task, then run full regression tests.

## 1. Stop generation and supplement input

### User-visible behavior

- While generation is active, replace Send with Stop.
- Stop cancels backend inference, not merely browser rendering.
- The original user message remains persisted and visible.
- The in-progress assistant response is removed completely from the UI and is never persisted to the database.
- Do not create an empty or partial assistant message; do not add an `INTERRUPTED` status or partial-response persistence mechanism.
- The user may submit additional information after stopping.
- Every user message remains a separate persisted row. The backend combines all unanswered user messages into one effective generation prompt without rewriting their stored contents.
- Multiple supplements and repeated stop/retry cycles must be deterministic and must not duplicate or silently consume messages.
- A successful assistant response marks the pending user-message set as answered.
- The cancelled partial assistant text must not enter future conversation history or context prompts.

### Persistence and state

- Replace the current "latest row is USER" heuristic with explicit generation/answer state or a reliable reply-to-message grouping.
- Retry and supplement behavior must distinguish a cancelled generation from a failed request and from a completed answer, without persisting cancelled assistant output.

### Cancellation and concurrency

- Use a server-side cancellation identity scoped to the authenticated user and conversation; do not trust a client-supplied conversation ID without ownership validation.
- Cancellation must be idempotent and must not cancel another conversation's or user's generation.
- Close/cancel the actual Ollama request and wait for the generation worker to terminate before releasing the global AI lock. Browser AbortController alone is insufficient.
- Handle disconnect, explicit Stop, Redis lock loss, Ollama errors, and normal completion as distinct outcomes.
- Do not hold a database transaction or connection during model inference.
- Validate race conditions: Stop just before completion, Stop while waiting for the global lock, reconnect, and repeated Stop.

## 2. Context usage monitor

### UI

Display near the composer:
- Remaining context tokens as the prominent absolute number.
- Used / total tokens.
- Usage percentage and progress bar.
- Green below 70%; yellow from 70% to below 90%; red at 90% and above.

### Measurement contract

- Capacity must come from the actual loaded model/runtime context configuration, not a hard-coded 32,768.
- The measured usage is the completed generation's actual prompt tokens plus generated response tokens. The prompt count includes system instructions, rendered chat history, pending user input, persistent context summary, retrieved knowledge excerpts, and template overhead.
- Reserve output capacity and a safety margin; 100% is not a target.
- Never label a character-based or unrelated-tokenizer estimate as exact.
- Ollama's documented chat/generate responses expose `prompt_eval_count` after prompt evaluation and `eval_count` for generated response tokens. Current public API documentation does not list a general `/api/tokenize` endpoint. Therefore investigate the deployed Ollama version and runtime for a model-compatible preflight tokenizer before promising draft-time exact counts. If no supported exact preflight is available, display the latest measured prompt plus generated-response token usage and clearly label any draft projection as an estimate—or omit the projection. Do not invent token counts.
- Handle model changes, runtime context changes, missing usage metadata, and stale measurements explicitly.

## 3. New conversation, context summary, title, and tree

### Creation flow

- Creating a continuation creates a new conversation ID; source conversation and messages remain unchanged.
- Generate a structured context summary from the selected source conversation.
- The user can inspect and edit the summary before confirming creation; provide an auto-generate action.
- Persist the confirmed summary on the new conversation as a context snapshot and include it in every future prompt for that conversation.
- Generate the new title from the summary/context. Allow the user to edit it.
- Store parent-child lineage; one parent may have multiple children.
- Show conversation lineage in chronological order in the history UI.
- Do not replay the entire parent transcript in every child prompt; use the persisted summary snapshot.

### Summary content

Preserve:
- Problem and goal.
- Relevant technical environment and facts.
- Decisions and constraints.
- Completed steps and observed results.
- Unresolved issues.
- Next action.

Do not include secrets, passwords, tokens, session cookies, or unrelated personal data. Treat source conversation text as untrusted input, not instructions to the summarization model.

### Data and API design requirements

- Decide between nullable `parent_conversation_id` plus summary columns on `conversations`, or a separate summary/version table, based on update/versioning requirements found during audit.
- Enforce same-owner parent references and prevent cycles.
- Preserve existing conversation list/message API compatibility where practical.
- Add ownership, validation, migration-upgrade, and migration-downgrade tests.

## Cross-cutting acceptance gates

- No paid external AI API; keep the current local Ollama provider.
- Maintain Finnish and English behavior.
- Preserve current RAG source validation and prompt-injection boundaries.
- No schema migration forks or multiple Alembic heads.
- No DB transaction held across inference.
- Test user isolation/IDOR, cancellation races, lock ownership, stream disconnects, persistence, retry, and conversation lineage.
- Update documentation only after test results are known. User has already reported post-merge testing on the previous baseline; that documentation update is separate from this feature work.
- Do not merge this branch without explicit user approval.


## Runtime verification note — Ollama cancellation

The backend cancels generation by closing the active HTTP response to Ollama and waits for the streaming worker to finish before releasing the Redis-backed generation/conversation locks. This follows Ollama's documented HTTP client-disconnect cancellation behavior, but the repository's Compose file currently uses the floating `ollama/ollama` image tag. Verify Stop Generation against the exact deployed Ollama image and confirm a second generation succeeds after cancellation. Upstream issue `ollama/ollama#17131` describes a streaming-handler goroutine/runner-slot leak on client disconnect; PR `#17135` was closed without being merged. Do not treat cancellation as fully runtime-verified until this integration check passes.\n\nThe cancellation registry is process-local. The current backend Dockerfile starts one Uvicorn worker; if the service is later scaled to multiple workers or replicas, replace the in-process registry with a distributed cancellation signal (for example Redis Pub/Sub) before scaling.

---

## 7. Implemented Conversation Lifecycle — Source-of-Truth Update (2026-11-13)

This section supersedes the earlier open design alternatives in Sections 3 and 4 where they conflict with the implementation recorded below. The current integration branch is feature/conversation-lifecycle at the time this update was prepared.

### Confirmed implementation

- Independent conversations are created by the sidebar New Conversation action without a parent reference or inherited context summary.
- Child conversations are created through a separate New Child Conversation composer action and a continuation-preview workflow.
- The preview returns an AI-generated title and context summary. The user can edit both before confirming creation.
- A child persists parent_conversation_id and context_summary on the conversations row. The database migration is backend/migrations/versions/0008_conversation_tree.py; the parent reference is a nullable self-referencing foreign key with ON DELETE SET NULL and an index.
- Child creation requires a title, a non-empty context summary, and an existing parent conversation owned by the same authenticated user. A summary without a parent is rejected by request validation.
- The saved summary is passed into later AI generation for the child. The parent's messages are not copied into the child transcript.
- The conversation list builds a hierarchical view and supports multiple children per parent.
- The New Child Conversation action is shown only when a conversation is active and the last completed generation has valid usage/capacity data with an exact usage ratio greater than 70%. Exactly 70% is hidden. This is not a live unsent-draft estimate.

### Verification status

The developer reported successful manual functional testing of independent and child conversation flows. Frontend build passed on Windows; frontend lint passed in Docker. Do not infer from this report that exact 70% boundary tests, all error paths, or all migration upgrade/downgrade scenarios have been independently verified.

### Documentation maintenance

For future approved structural or technical changes, update both docs.eng/docs/ and docs.suomi/docs/ in the same documentation change. Update only the documents affected by the change, but check requirements, user stories/acceptance criteria, backlog, Sprint plan, system design, UX/UI design, and project-management decision/change logs for consistency. Treat source code and migrations as the implementation authority; treat these documents as the synchronized project specification and history.

