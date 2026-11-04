import json
import unittest
from unittest.mock import patch

from app.ai import GeneratedReply, GeneratedTicketDraft, OllamaUnavailableError, generate_reply, generate_reply_stream, generate_ticket_draft, preload_model


def ollama_response(content: str) -> object:
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self) -> bytes:
            return json.dumps({"message": {"content": content}}).encode()

    return FakeResponse()


class OllamaResponseTests(unittest.TestCase):
    def test_preload_requests_model_without_generation_and_keeps_it_loaded(self) -> None:
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self) -> bytes:
                return json.dumps({"done": True, "response": ""}).encode()

        with (
            patch("app.ai.OLLAMA_BASE_URL", "http://localhost:11434"),
            patch("app.ai.urlopen", return_value=FakeResponse()) as urlopen,
        ):
            preload_model()

        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "http://localhost:11434/api/generate")
        self.assertEqual(
            json.loads(request.data),
            {"model": "poro-helpdesk", "keep_alive": "24h"},
        )

    def test_invalid_preload_response_is_reported_as_unavailable(self) -> None:
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self) -> bytes:
                return json.dumps({"done": False}).encode()

        with (
            patch("app.ai.urlopen", return_value=FakeResponse()),
            self.assertRaises(OllamaUnavailableError),
        ):
            preload_model()

    def test_malformed_message_payload_is_reported_as_unavailable(self) -> None:
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self) -> bytes:
                return json.dumps({"message": None}).encode()

        with patch("app.ai.urlopen", return_value=FakeResponse()):
            with self.assertRaises(OllamaUnavailableError):
                generate_reply([{"role": "user", "content": "Help"}])

    def test_reply_uses_language_preference_and_returns_updated_preference(self) -> None:
        responses = [
            ollama_response(
                json.dumps(
                    {"input_language": "English", "requested_language": "French"}
                )
            ),
            ollama_response(json.dumps({"reply": "Bonjour !", "source_ids": []})),
        ]
        with patch("app.ai.urlopen", side_effect=responses) as urlopen:
            result = generate_reply(
                [{"role": "user", "content": "Please answer in French from now on."}],
                "Finnish",
            )

        self.assertEqual(result, GeneratedReply("Bonjour !", "French"))
        classification_payload = json.loads(urlopen.call_args_list[0].args[0].data)
        reply_payload = json.loads(urlopen.call_args_list[1].args[0].data)
        self.assertIn(
            "never copy input_language into requested_language",
            classification_payload["messages"][0]["content"],
        )
        self.assertEqual(classification_payload["format"]["type"], "object")
        self.assertIn(
            "MANDATORY RESPONSE LANGUAGE: French.",
            reply_payload["messages"][0]["content"],
        )

    def test_invalid_structured_reply_is_reported_as_unavailable(self) -> None:
        with (
            patch(
                "app.ai.urlopen",
                side_effect=[
                    ollama_response(
                        json.dumps(
                            {"input_language": "English", "requested_language": None}
                        )
                    ),
                    ollama_response("Bonjour !"),
                ],
            ),
            self.assertRaises(OllamaUnavailableError),
        ):
            generate_reply([{"role": "user", "content": "Help"}])

    def test_other_input_language_defaults_to_english(self) -> None:
        with patch(
            "app.ai.urlopen",
            side_effect=[
                ollama_response(
                    json.dumps({"input_language": "other", "requested_language": None})
                ),
                ollama_response(json.dumps({"reply": "DNS is a naming system.", "source_ids": []})),
            ],
        ) as urlopen:
            result = generate_reply([{"role": "user", "content": "¿Qué es DNS?"}])

        reply_payload = json.loads(urlopen.call_args_list[1].args[0].data)
        self.assertEqual(result, GeneratedReply("DNS is a naming system.", None))
        self.assertIn(
            "MANDATORY RESPONSE LANGUAGE: English.",
            reply_payload["messages"][0]["content"],
        )

    def test_invalid_language_classification_is_reported_as_unavailable(self) -> None:
        with (
            patch(
                "app.ai.urlopen",
                return_value=ollama_response(
                    json.dumps(
                        {"input_language": [], "requested_language": None}
                    )
                ),
            ),
            self.assertRaises(OllamaUnavailableError),
        ):
            generate_reply([{"role": "user", "content": "Help"}])

    def test_saved_preference_is_kept_when_user_does_not_change_it(self) -> None:
        with patch(
            "app.ai.urlopen",
            side_effect=[
                ollama_response(
                    json.dumps({"input_language": "English", "requested_language": None})
                ),
                ollama_response(json.dumps({"reply": "Bonjour.", "source_ids": []})),
            ],
        ) as urlopen:
            result = generate_reply(
                [{"role": "user", "content": "What is DNS?"}],
                "French",
            )

        reply_payload = json.loads(urlopen.call_args_list[1].args[0].data)
        self.assertEqual(result, GeneratedReply("Bonjour.", "French"))
        self.assertIn(
            "MANDATORY RESPONSE LANGUAGE: French.",
            reply_payload["messages"][0]["content"],
        )

    def test_non_object_response_is_reported_as_unavailable(self) -> None:
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self) -> bytes:
                return json.dumps([]).encode()

        with patch("app.ai.urlopen", return_value=FakeResponse()):
            with self.assertRaises(OllamaUnavailableError):
                generate_reply([{"role": "user", "content": "Help"}])


    def test_streaming_reply_yields_incremental_text_and_saved_language(self) -> None:
        class StreamResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def __iter__(self):
                chunks = [
                    {"message": {"content": "First "}, "done": False},
                    {"message": {"content": "second."}, "done": False},
                    {"message": {"content": ""}, "done": True},
                ]
                return iter((json.dumps(item) + "\n").encode() for item in chunks)

        with patch(
            "app.ai.urlopen",
            side_effect=[
                ollama_response(
                    json.dumps({"input_language": "English", "requested_language": None})
                ),
                StreamResponse(),
            ],
        ) as urlopen:
            events = list(generate_reply_stream(
                [{"role": "user", "content": "Explain DNS"}],
                "Finnish",
            ))

        content_chunks = [value for kind, value in events if kind == "content"]
        self.assertGreater(len(content_chunks), 1)
        self.assertEqual("".join(content_chunks), "First second.")
        self.assertEqual(events[0], ("language", "Finnish"))
        self.assertEqual(events[-2:], [
            ("sources", []),
            ("ticket_recommendation", False),
        ])
        payload = json.loads(urlopen.call_args_list[1].args[0].data)
        self.assertIs(payload["stream"], True)
        self.assertIn("MANDATORY RESPONSE LANGUAGE: Finnish.", payload["messages"][0]["content"])


    def test_ticket_draft_is_structured_concise_and_uses_conversation_language(self) -> None:
        draft_json = json.dumps({
            "title": "Wi-Fi disconnects every few minutes",
            "description": "Problem: The Wi-Fi connection disconnects every few minutes.\nTried: Restarting the router did not help.",
        })
        messages = [
            {"role": "user", "content": "My Wi-Fi keeps disconnecting."},
            {"role": "assistant", "content": "Have you restarted the router?"},
            {"role": "user", "content": "Yes, but it still disconnects."},
        ]
        with patch("app.ai.urlopen", return_value=ollama_response(draft_json)) as urlopen:
            result = generate_ticket_draft(messages, "English")

        self.assertEqual(result, GeneratedTicketDraft(
            "Wi-Fi disconnects every few minutes",
            "Problem: The Wi-Fi connection disconnects every few minutes.\nTried: Restarting the router did not help.",
        ))
        payload = json.loads(urlopen.call_args.args[0].data)
        self.assertIn("Do not invent causes", payload["messages"][0]["content"])
        self.assertIn("English", payload["messages"][0]["content"])
        self.assertEqual(payload["messages"][1], messages[0])
        self.assertEqual(payload["messages"][2], messages[1])
        self.assertEqual(payload["messages"][-1]["role"], "user")
        self.assertIn("not a transcript or dialogue", payload["messages"][-1]["content"])
        self.assertEqual(payload["format"]["required"], ["title", "description"])

    def test_ticket_draft_rejects_invalid_or_empty_fields(self) -> None:
        with (
            patch("app.ai.urlopen", return_value=ollama_response(json.dumps({"title": "", "description": ""}))),
            self.assertRaises(OllamaUnavailableError),
        ):
            generate_ticket_draft([{"role": "user", "content": "Help"}])

    def test_streaming_reply_hides_ticket_recommendation_marker(self) -> None:
        marker = "[TICKET_RECOMMENDED]"
        class StreamResponse:
            def __enter__(self): return self
            def __exit__(self, *_args): return False
            def __iter__(self):
                chunks = [
                    {"message": {"content": "I could not solve this reliably. "}, "done": False},
                    {"message": {"content": "Please create a support ticket.\n[TICKET_"}, "done": False},
                    {"message": {"content": "RECOMMENDED]"}, "done": False},
                    {"message": {"content": ""}, "done": True},
                ]
                return iter((json.dumps(item) + "\n").encode() for item in chunks)
        with patch("app.ai.urlopen", side_effect=[
            ollama_response(json.dumps({"input_language": "English", "requested_language": None})),
            StreamResponse(),
        ]):
            events = list(generate_reply_stream([{"role": "user", "content": "Nothing works"}]))
        content = "".join(value for kind, value in events if kind == "content").strip()
        self.assertEqual(content, "I could not solve this reliably. Please create a support ticket.")
        self.assertEqual(events[-1], ("ticket_recommendation", True))
        self.assertNotIn(marker, content)


    def test_ticket_draft_rejects_a_copied_first_question_and_transcript(self) -> None:
        messages = [
            {"role": "user", "content": "The application crashes on startup."},
            {"role": "assistant", "content": "Try restarting the application."},
            {"role": "user", "content": "I restarted it and it still crashes."},
        ]
        copied = json.dumps({
            "title": "The application crashes on startup.",
            "description": "The application crashes on startup. Try restarting the application. I restarted it and it still crashes.",
        })
        with (
            patch("app.ai.urlopen", return_value=ollama_response(copied)),
            self.assertRaises(OllamaUnavailableError),
        ):
            generate_ticket_draft(messages, "English")
