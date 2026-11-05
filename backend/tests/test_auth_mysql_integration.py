"""Opt-in registration and concurrent sign-in checks against the Compose MySQL DB.

Run inside the backend container with RUN_AUTH_MYSQL_INTEGRATION=1. The test
creates a uniquely named account and removes only that account and its sessions.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import os
import secrets
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from sqlalchemy import delete, func, select

from app.database import SessionLocal
from app.models import AuthSession, User


API_ROOT = os.getenv("AUTH_TEST_API_ROOT", "http://127.0.0.1:8000/api/v1")
FRONTEND_ORIGIN = os.getenv("AUTH_TEST_ORIGIN", "http://localhost:8088")


def request_json(path: str, payload: dict[str, str] | None = None, cookie: str | None = None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Origin": FRONTEND_ORIGIN}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if cookie is not None:
        headers["Cookie"] = cookie
    request = Request(f"{API_ROOT}{path}", data=body, headers=headers, method="GET" if body is None else "POST")
    try:
        with urlopen(request, timeout=60) as response:
            return response.status, response.headers, json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return error.code, error.headers, json.loads(error.read().decode("utf-8"))


@unittest.skipUnless(
    os.getenv("RUN_AUTH_MYSQL_INTEGRATION") == "1",
    "requires the running Compose backend and MySQL; opt in with RUN_AUTH_MYSQL_INTEGRATION=1",
)
class AuthMySQLIntegrationTests(unittest.TestCase):
    def test_register_then_concurrent_signins_create_valid_mysql_sessions(self) -> None:
        suffix = secrets.token_hex(8)
        email = f"auth-check-{suffix}@example.invalid"
        username = f"authcheck{suffix}"
        password = "Integration-test-Password-2026"
        registration = {
            "first_name": "Integration",
            "last_name": "Check",
            "username": username,
            "email": email,
            "password": password,
        }
        user_id: int | None = None

        try:
            status_code, _, result = request_json("/auth/register", registration)
            self.assertEqual(status_code, 201, result)
            user_id = result["user"]["id"]
            self.assertEqual(result["user"]["email"], email)

            concurrency = 8
            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                signins = list(executor.map(
                    lambda _index: request_json("/auth/login", {"email": email, "password": password}),
                    range(concurrency),
                ))

            cookies: list[str] = []
            for status_code, headers, body in signins:
                self.assertEqual(status_code, 200, body)
                self.assertTrue(body["authenticated"])
                self.assertFalse(body["must_change_password"])
                set_cookie = headers.get("Set-Cookie", "")
                cookie = set_cookie.split(";", 1)[0]
                self.assertTrue(cookie.startswith("ai_helpdesk_session="), set_cookie)
                cookies.append(cookie)

            for cookie in cookies:
                status_code, _, body = request_json("/auth/me", cookie=cookie)
                self.assertEqual(status_code, 200, body)
                self.assertTrue(body["authenticated"])

            with SessionLocal() as db:
                session_count = db.scalar(
                    select(func.count(AuthSession.id)).where(AuthSession.user_id == user_id)
                )
            self.assertEqual(session_count, concurrency)
        finally:
            if user_id is not None:
                with SessionLocal() as db:
                    db.execute(delete(AuthSession).where(AuthSession.user_id == user_id))
                    db.execute(delete(User).where(User.id == user_id))
                    db.commit()


if __name__ == "__main__":
    unittest.main()
