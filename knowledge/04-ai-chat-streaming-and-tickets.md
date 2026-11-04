# AI HelpDesk — AI Chat, Streaming and Ticket Creation

- **Document ID:** KB-PROJECT-04
- **Status:** verified from `backend/app/ai.py`, `backend/app/main.py`, `frontend/src/pages/ChatPage.tsx` and US-09 project criteria; RAG integration remains planned
- **Applies to:** Ollama chat, conversation history, stream protocol, US-09
- **Keywords:** Ollama, LLM, chat, conversation, message, NDJSON, streaming, retry, ticket draft, US-09, tekoälychat, keskustelu, viestivirta, tukipyynnön luonti

## Model and backend integration

The backend calls Ollama's HTTP API at the configured base URL. The model name defaults to `poro-helpdesk`. The selected GGUF artifact is `Llama-Poro-2-8B-Instruct.Q4_K_M.gguf`. The Modelfile sets `num_ctx 4096` and `temperature 0.2`.

At backend startup, the FastAPI lifespan pings Redis and attempts to preload the configured Ollama model. It retries the preload while Ollama is unavailable. Therefore, backend startup readiness depends on Redis and successful model preload.

## Language handling

The AI module first asks the model to classify the latest user message as Finnish, English or other, and to identify an explicitly requested response language. It then constructs a system prompt requiring the response language. The streaming path emits a language event before content.

The frontend's UI language and the AI response language are related but distinct concepts. The frontend stores its UI choice as `fi` or `en`; the backend also reasons about the language of the conversation and explicit language requests.

## Conversation persistence

User and assistant messages are stored in MySQL and associated with a conversation. The frontend loads conversation history from the backend. The backend must verify that the conversation belongs to the authenticated user before returning or changing its messages.

## Streaming protocol

The frontend sends a POST request to:
`/api/v1/conversations/{conversation_id}/messages/stream`

The response body is a newline-delimited stream of JSON events (NDJSON). The reviewed frontend handles event names:
- `user_message`: confirms the persisted user message and replaces its optimistic temporary message.
- `token`: appends an assistant text chunk.
- `done`: finalizes the assistant message and carries the ticket-recommendation flag.
- `error`: indicates a stream failure; may include the saved user message ID or error detail.

The frontend reads the response with `ReadableStream.getReader()`, `TextDecoder`, and a text buffer. A network chunk is not guaranteed to end at a JSON line boundary, so the client buffers partial lines and parses only complete lines. It processes a final non-empty buffer after the stream closes.

Do not confuse NDJSON with Server-Sent Events (SSE). This implementation uses newline-delimited JSON over a streaming HTTP response, not the browser EventSource protocol.

## Optimistic UI and retry

The frontend displays a temporary user message before the server confirms persistence. When the server emits `user_message`, the temporary ID is replaced with the saved database message.

If failure occurs before persistence, the frontend restores the draft so the user can try again. If the user message was saved but AI generation failed, the saved user message remains and the UI offers a separate retry action. The user should retry that saved message instead of submitting the same text as a new message.

The backend uses a Redis per-conversation lock with a random token and expiring lease to prevent overlapping generations. The lease is renewed while generation continues. Release and renewal scripts compare the token so one request cannot release another request's lock.

## US-09: create a ticket from a conversation

The intended and implemented workflow is:
1. The user has a saved conversation.
2. The frontend requests a ticket draft from the conversation.
3. The backend sends role-preserving conversation messages to Ollama and asks for a specific title and concise technician-facing summary.
4. The model must not invent facts or describe assistant suggestions as steps the user has already performed.
5. The frontend displays editable title, description and priority fields.
6. The user reviews/edits the draft and explicitly confirms creation.
7. The backend derives ticket ownership from the authenticated session and verifies that the conversation belongs to that same user.
8. The ticket is saved with its conversation reference.

Canceling or closing the draft editor must not create a ticket. This is a hard acceptance criterion, not a UI preference.

The ticket-generation prompt treats conversation content as untrusted source material, not instructions. It rejects a generated title that merely repeats the first user question and rejects summaries that closely reproduce the transcript. It must not include passwords, tokens or other secrets.

## Ticket recommendation

The AI prompt may append an internal marker `[TICKET_RECOMMENDED]` or `[NO_TICKET_RECOMMENDATION]`. The backend strips this marker from visible text and exposes a boolean recommendation signal. The marker is machine metadata, not user-facing prose.

## RAG status

At the reviewed repository snapshot, `backend/app/ai.py` did not yet contain Markdown/TXT keyword retrieval or prompt integration, and the backend did not expose the planned knowledge-search endpoint. Do not claim that current chat answers already use the Knowledge Base until the implementation and tests are merged.
