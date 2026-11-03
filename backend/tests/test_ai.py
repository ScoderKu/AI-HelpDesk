import json
import unittest
from unittest.mock import patch

from app.ai import GeneratedReply, OllamaUnavailableError, generate_reply, generate_reply_stream, preload_model


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

        with patch("app.ai.urlopen", return_value=FakeResponse()) as urlopen:
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
            ollama_response(json.dumps({"reply": "Bonjour !"})),
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
                ollama_response(json.dumps({"reply": "DNS is a naming system."})),
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
                ollama_response(json.dumps({"reply": "Bonjour."})),
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
                return iter((json.dumps(item) + "\\n").encode() for item in chunks)

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

        self.assertEqual(events, [
            ("language", "Finnish"),
            ("content", "First "),
            ("content", "second."),
        ])
        payload = json.loads(urlopen.call_args_list[1].args[0].data)
        self.assertIs(payload["stream"], True)
        self.assertIn("MANDATORY RESPONSE LANGUAGE: Finnish.", payload["messages"][0]["content"])
