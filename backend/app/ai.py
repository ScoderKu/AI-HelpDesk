"""Ollama client used by the AI HelpDesk backend."""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "poro-helpdesk")
OLLAMA_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "90"))
MAX_CONTEXT_MESSAGES = 20
SYSTEM_PROMPT = (
    "You are the AI HelpDesk technical support assistant. "
    "Reply in the language used by the user (Finnish or English). "
    "Give clear, safe, step-by-step troubleshooting guidance. "
    "Ask one relevant clarifying question when essential information is missing. "
    "Never claim to have changed anything or created a support ticket. "
    "Never ask for passwords, one-time codes, or other secrets."
)


class OllamaUnavailableError(Exception):
    """Ollama could not be reached or did not return a valid response."""


def generate_reply(messages: list[dict[str, str]]) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages[-MAX_CONTEXT_MESSAGES:],
        ],
        "stream": False,
    }
    request = Request(
        f"{OLLAMA_BASE_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=OLLAMA_TIMEOUT_SECONDS) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as error:
        raise OllamaUnavailableError(type(error).__name__) from None

    content = result.get("message", {}).get("content")
    if not isinstance(content, str) or not content.strip():
        raise OllamaUnavailableError("Invalid response from Ollama")
    return content.strip()
