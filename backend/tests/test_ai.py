import json
import unittest
from unittest.mock import patch

from app.ai import OllamaUnavailableError, generate_reply


class OllamaResponseTests(unittest.TestCase):
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
