import os
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")
os.environ.setdefault("MYSQL_DATABASE", "test")

from fastapi import HTTPException, Request, Response
from redis.exceptions import RedisError

from app import main
from app.schemas import UserLoginRequest


def make_request(peer_ip: str = "192.0.2.10") -> Request:
    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "method": "POST",
            "scheme": "http",
            "path": "/api/v1/auth/login",
            "raw_path": b"/api/v1/auth/login",
            "query_string": b"",
            "headers": [],
            "client": (peer_ip, 12345),
            "server": ("localhost", 8000),
        }
    )


class LoginRateLimitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = make_request()
        self.email = "user@example.com"

    def test_attempt_check_increments_ip_and_only_reads_account_failures(self) -> None:
        with (
            patch.object(main, "get_client_ip", return_value="192.0.2.10"),
            patch.object(main, "get_session_secret", return_value=b"s" * 32),
            patch.object(
                main.redis_client,
                "eval",
                return_value=[1, 2, 59, 700],
            ) as eval_script,
        ):
            main.enforce_login_rate_limit(self.request, self.email)

        script = eval_script.call_args.args[0]
        self.assertIn("redis.call('INCR', KEYS[1])", script)
        self.assertIn("redis.call('GET', KEYS[2])", script)
        self.assertNotIn("redis.call('INCR', KEYS[2])", script)
        self.assertEqual(eval_script.call_args.args[1], 2)

    def test_blocks_ip_after_twenty_requests(self) -> None:
        with (
            patch.object(main, "get_client_ip", return_value="192.0.2.10"),
            patch.object(main, "get_session_secret", return_value=b"s" * 32),
            patch.object(main.redis_client, "eval", return_value=[21, 0, 42, -2]),
        ):
            with self.assertRaises(HTTPException) as raised:
                main.enforce_login_rate_limit(self.request, self.email)

        self.assertEqual(raised.exception.status_code, 429)
        self.assertEqual(raised.exception.headers["Retry-After"], "42")

    def test_blocks_account_after_five_failed_logins(self) -> None:
        with (
            patch.object(main, "get_client_ip", return_value="192.0.2.10"),
            patch.object(main, "get_session_secret", return_value=b"s" * 32),
            patch.object(main.redis_client, "eval", return_value=[1, 5, 59, 700]),
        ):
            with self.assertRaises(HTTPException) as raised:
                main.enforce_login_rate_limit(self.request, self.email)

        self.assertEqual(raised.exception.status_code, 429)
        self.assertEqual(raised.exception.headers["Retry-After"], "700")

    def test_records_failed_login_with_expiring_account_counter(self) -> None:
        with (
            patch.object(main, "get_session_secret", return_value=b"s" * 32),
            patch.object(main.redis_client, "eval", return_value=[1, 900]) as eval_script,
        ):
            main.record_failed_login(self.email)

        script = eval_script.call_args.args[0]
        self.assertIn("redis.call('INCR', KEYS[1])", script)
        self.assertIn("redis.call('EXPIRE', KEYS[1], ARGV[1])", script)
        self.assertEqual(eval_script.call_args.args[1], 1)
        self.assertEqual(eval_script.call_args.args[3], main.LOGIN_ACCOUNT_WINDOW_SECONDS)

    def test_concurrent_sixth_failure_is_rate_limited(self) -> None:
        with (
            patch.object(main, "get_session_secret", return_value=b"s" * 32),
            patch.object(main.redis_client, "eval", return_value=[6, 840]),
        ):
            with self.assertRaises(HTTPException) as raised:
                main.record_failed_login(self.email)

        self.assertEqual(raised.exception.status_code, 429)
        self.assertEqual(raised.exception.headers["Retry-After"], "840")

    def test_redis_failure_fails_closed(self) -> None:
        with (
            patch.object(main, "get_client_ip", return_value="192.0.2.10"),
            patch.object(main, "get_session_secret", return_value=b"s" * 32),
            patch.object(
                main.redis_client,
                "eval",
                side_effect=RedisError("offline"),
            ),
        ):
            with self.assertRaises(HTTPException) as raised:
                main.enforce_login_rate_limit(self.request, self.email)

        self.assertEqual(raised.exception.status_code, 503)

    def test_redis_failure_while_recording_bad_password_fails_closed(self) -> None:
        with (
            patch.object(main, "get_session_secret", return_value=b"s" * 32),
            patch.object(
                main.redis_client,
                "eval",
                side_effect=RedisError("offline"),
            ),
        ):
            with self.assertRaises(HTTPException) as raised:
                main.record_failed_login(self.email)

        self.assertEqual(raised.exception.status_code, 503)

    def test_successful_login_does_not_record_email_failure(self) -> None:
        user = SimpleNamespace(
            id=7,
            first_name="Ada",
            last_name="Lovelace",
            username="ada",
            email=self.email,
            password_hash="stored-hash",
        )
        db = MagicMock()
        db.scalar.return_value = user
        credentials = UserLoginRequest(email=self.email, password="correct-pass")

        with (
            patch.object(main, "enforce_login_rate_limit") as check_limit,
            patch.object(main, "get_session_secret", return_value=b"s" * 32),
            patch.object(main, "verify_password", return_value=True),
            patch.object(main, "record_failed_login") as record_failure,
        ):
            result = main.login_user(
                credentials,
                self.request,
                Response(),
                db,
            )

        check_limit.assert_called_once_with(self.request, self.email)
        record_failure.assert_not_called()
        db.commit.assert_called_once_with()
        self.assertEqual(result.username, "ada")

    def test_failed_login_records_account_failure(self) -> None:
        user = SimpleNamespace(password_hash="stored-hash")
        db = MagicMock()
        db.scalar.return_value = user
        credentials = UserLoginRequest(email=self.email, password="wrong-pass")

        with (
            patch.object(main, "enforce_login_rate_limit"),
            patch.object(main, "verify_password", return_value=False),
            patch.object(main, "record_failed_login") as record_failure,
        ):
            with self.assertRaises(HTTPException) as raised:
                main.login_user(credentials, self.request, Response(), db)

        self.assertEqual(raised.exception.status_code, 401)
        record_failure.assert_called_once_with(self.email)
        db.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
