import asyncio
import os
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")
os.environ.setdefault("MYSQL_DATABASE", "test")

from fastapi import Request
from starlette.responses import Response

from app import main


def make_request(method="GET", path="/api/v1/users/me", headers=None, client=("127.0.0.1", 1234)):
    return Request({
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": headers or [],
        "client": client,
        "server": ("testserver", 80),
    })


class RegistrationRateLimitTests(unittest.TestCase):
    def test_registration_rate_limit_returns_retry_after(self):
        request = make_request(headers=[(b"x-forwarded-for", b"203.0.113.10")])
        with patch.object(main.redis_client, "eval", return_value=[6, 120]) as evaluate:
            with self.assertRaises(main.HTTPException) as raised:
                main.enforce_registration_rate_limit(request)

        self.assertEqual(raised.exception.status_code, 429)
        self.assertEqual(raised.exception.headers["Retry-After"], "120")
        self.assertEqual(evaluate.call_args.args[0], main.REGISTER_ATTEMPT_SCRIPT)

    def test_registration_rate_limit_fails_closed_when_redis_is_down(self):
        from redis.exceptions import RedisError

        with patch.object(main.redis_client, "eval", side_effect=RedisError("offline")):
            with self.assertRaises(main.HTTPException) as raised:
                main.enforce_registration_rate_limit(make_request())

        self.assertEqual(raised.exception.status_code, 503)


class GlobalAiLockTests(unittest.TestCase):
    def test_global_lock_rejects_concurrent_generation(self):
        with patch.object(main.redis_client, "set", return_value=None):
            with self.assertRaises(main.HTTPException) as raised:
                with main.lock_ai_generation():
                    self.fail("A busy global lock must not be acquired")

        self.assertEqual(raised.exception.status_code, 429)
        self.assertEqual(raised.exception.headers["Retry-After"], "5")

    def test_global_lock_releases_only_its_own_token(self):
        with (
            patch.object(main.redis_client, "set", return_value=True),
            patch.object(main.redis_client, "eval", return_value=1) as evaluate,
        ):
            with main.lock_ai_generation():
                pass

        self.assertEqual(evaluate.call_args.args[0], main.RELEASE_CHAT_LOCK_SCRIPT)
        self.assertEqual(evaluate.call_args.args[2], "ai:generation:global")


class ApiSecurityMiddlewareTests(unittest.TestCase):
    def test_cookie_authenticated_unsafe_request_rejects_untrusted_origin(self):
        request = make_request(
            method="PATCH",
            headers=[
                (b"cookie", b"ai_helpdesk_session=present"),
                (b"origin", b"https://attacker.example"),
            ],
        )
        called = False

        async def call_next(_request):
            nonlocal called
            called = True
            return Response("ok")

        response = asyncio.run(main.apply_api_security_headers(request, call_next))
        self.assertEqual(response.status_code, 403)
        self.assertFalse(called)
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_api_responses_get_private_cache_and_security_headers(self):
        request = make_request()

        async def call_next(_request):
            return Response("ok")

        response = asyncio.run(main.apply_api_security_headers(request, call_next))
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertEqual(response.headers["Referrer-Policy"], "strict-origin-when-cross-origin")


if __name__ == "__main__":
    unittest.main()
