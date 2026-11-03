import os
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")
os.environ.setdefault("MYSQL_DATABASE", "test")

from fastapi import HTTPException, Request, Response
from pydantic import ValidationError

from app import main
from app.models import User
from app.schemas import UserPasswordChangeRequest, UserProfileUpdateRequest


class UserProfileSchemaTests(unittest.TestCase):
    def test_profile_accepts_username_as_the_only_editable_field(self) -> None:
        request = UserProfileUpdateRequest(username=" ada ")
        self.assertEqual(request.model_dump(), {"username": "ada"})
        with self.assertRaises(ValidationError):
            UserProfileUpdateRequest(
                username="ada",
                first_name="Changed",
            )

    def test_profile_accepts_partial_updates(self) -> None:
        request = UserProfileUpdateRequest(username=" newname ")
        self.assertEqual(request.model_dump(exclude_unset=True), {"username": "newname"})
        self.assertEqual(request.model_fields_set, {"username"})

    def test_profile_rejects_empty_patch_nulls_and_invalid_supplied_values(self) -> None:
        invalid_payloads = (
            {},
            {"username": None},
            {"first_name": "Ada"},
            {"last_name": "Lovelace"},
            {"username": "ab"},
        )
        for values in invalid_payloads:
            with self.subTest(values=values), self.assertRaises(ValidationError):
                UserProfileUpdateRequest(**values)

    def test_password_change_requires_matching_confirmation_and_distinct_password(self) -> None:
        valid = UserPasswordChangeRequest(
            current_password="current-pass",
            new_password="new-password",
            confirm_new_password="new-password",
        )
        self.assertEqual(valid.new_password.get_secret_value(), "new-password")
        with self.assertRaises(ValidationError):
            UserPasswordChangeRequest(
                current_password="current-pass",
                new_password="new-password",
                confirm_new_password="different-password",
            )
        with self.assertRaises(ValidationError):
            UserPasswordChangeRequest(
                current_password="same-password",
                new_password="same-password",
                confirm_new_password="same-password",
            )


class UserProfileEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User(
            id=7,
            first_name="Ada",
            last_name="Lovelace",
            username="ada",
            email="ada@example.com",
            password_hash="stored-hash",
            must_change_password=False,
        )

    def test_profile_routes_require_authenticated_user(self) -> None:
        expected = {
            ("GET", "/api/v1/users/me"),
            ("PATCH", "/api/v1/users/me"),
            ("POST", "/api/v1/users/me/password"),
        }
        for route in main.app.routes:
            if not isinstance(route, main.app.router.route_class):
                continue
            for method in route.methods or ():
                key = (method, route.path)
                if key in expected:
                    dependencies = {
                        dependency.call for dependency in route.dependant.dependencies
                    }
                    self.assertIn(main.get_authenticated_user, dependencies)
                    expected.remove(key)
        self.assertFalse(expected)

    def test_profile_read_returns_user_fields_without_password_hash(self) -> None:
        response = main.get_current_user_profile(MagicMock(), self.user)
        payload = response.model_dump()
        self.assertEqual(payload["email"], "ada@example.com")
        self.assertEqual(payload["username"], "ada")
        self.assertNotIn("password_hash", payload)

    def test_profile_update_changes_only_supplied_fields(self) -> None:
        db = MagicMock()
        db.scalar.return_value = None
        request = UserProfileUpdateRequest(username="augusta")
        result = main.update_current_user_profile(request, self.user, db)
        self.assertEqual(result.first_name, "Ada")
        self.assertEqual(result.last_name, "Lovelace")
        self.assertEqual(result.username, "augusta")
        self.assertEqual(result.email, "ada@example.com")
        db.scalar.assert_called_once()
        db.commit.assert_called_once_with()
        db.refresh.assert_called_once_with(self.user)

    def test_profile_update_rejects_username_owned_by_another_user(self) -> None:
        db = MagicMock()
        db.scalar.return_value = 99
        with self.assertRaises(HTTPException) as raised:
            main.update_current_user_profile(
                UserProfileUpdateRequest(username="taken"),
                self.user,
                db,
            )
        self.assertEqual(raised.exception.status_code, 409)
        db.commit.assert_not_called()

    @patch("app.main.hash_password", return_value="new-hash")
    @patch("app.main.verify_password", return_value=True)
    def test_password_change_hashes_new_password_and_revokes_sessions(
        self, verify: MagicMock, hash_new: MagicMock
    ) -> None:
        db = MagicMock()
        db.scalar.return_value = self.user
        response = main.change_current_user_password(
            UserPasswordChangeRequest(
                current_password="current-password",
                new_password="new-password",
                confirm_new_password="new-password",
            ),
            self.user,
            db,
        )
        self.assertEqual(self.user.password_hash, "new-hash")
        self.assertFalse(self.user.must_change_password)
        verify.assert_called_once_with("current-password", "stored-hash")
        hash_new.assert_called_once_with("new-password")
        db.execute.assert_called_once()
        db.commit.assert_called_once_with()
        self.assertEqual(response.status_code, 204)
        self.assertIn("ai_helpdesk_session", response.headers.get("set-cookie", ""))

    @patch("app.main.verify_password", return_value=False)
    def test_password_change_rejects_incorrect_current_password(
        self, verify: MagicMock
    ) -> None:
        db = MagicMock()
        with self.assertRaises(HTTPException) as raised:
            main.change_current_user_password(
                UserPasswordChangeRequest(
                    current_password="wrong-password",
                    new_password="new-password",
                    confirm_new_password="new-password",
                ),
                self.user,
                db,
            )
        self.assertEqual(raised.exception.status_code, 400)
        db.commit.assert_not_called()

    def test_temporary_password_session_allows_auth_status_and_password_change(self) -> None:
        self.user.must_change_password = True
        db = MagicMock()
        db.scalar.return_value = "session-id"
        db.get.return_value = self.user

        for method, path in (
            ("GET", "/api/v1/auth/me"),
            ("POST", "/api/v1/users/me/password"),
        ):
            request = Request({
                "type": "http",
                "http_version": "1.1",
                "method": method,
                "scheme": "http",
                "path": path,
                "raw_path": path.encode(),
                "query_string": b"",
                "headers": [],
                "client": ("127.0.0.1", 12345),
                "server": ("localhost", 8000),
            })
            with self.subTest(method=method, path=path), patch(
                "app.main.get_session_claims",
                return_value=(self.user.id, 2_000_000_000, "a" * 32),
            ):
                self.assertIs(main.get_authenticated_user(request, db), self.user)

    def test_temporary_password_session_cannot_access_other_protected_routes(self) -> None:
        self.user.must_change_password = True
        db = MagicMock()
        db.scalar.return_value = "session-id"
        db.get.return_value = self.user

        for method, path in (
            ("GET", "/api/v1/users/me"),
            ("PATCH", "/api/v1/users/me"),
            ("GET", "/api/v1/tickets"),
        ):
            request = Request({
                "type": "http",
                "http_version": "1.1",
                "method": method,
                "scheme": "http",
                "path": path,
                "raw_path": path.encode(),
                "query_string": b"",
                "headers": [],
                "client": ("127.0.0.1", 12345),
                "server": ("localhost", 8000),
            })
            with (
                self.subTest(method=method, path=path),
                patch(
                    "app.main.get_session_claims",
                    return_value=(self.user.id, 2_000_000_000, "a" * 32),
                ),
                self.assertRaises(HTTPException) as raised,
            ):
                main.get_authenticated_user(request, db)

            self.assertEqual(raised.exception.status_code, 403)

    def test_logout_accepts_configured_origin_and_rejects_untrusted_origin(self) -> None:
        db = MagicMock()
        db.scalar.return_value = None

        def make_logout_request(origin: str) -> Request:
            path = "/api/v1/auth/logout"
            return Request({
                "type": "http",
                "http_version": "1.1",
                "method": "POST",
                "scheme": "http",
                "path": path,
                "raw_path": path.encode(),
                "query_string": b"",
                "headers": [(b"origin", origin.encode())],
                "client": ("127.0.0.1", 12345),
                "server": ("localhost", 8000),
            })

        with patch("app.main.get_session_claims", return_value=None):
            response = main.logout_user(
                make_logout_request(main.FRONTEND_ORIGINS[0]),
                Response(),
                db,
            )

        self.assertEqual(response.status_code, 204)
        self.assertIn("ai_helpdesk_session", response.headers.get("set-cookie", ""))

        with self.assertRaises(HTTPException) as raised:
            main.logout_user(
                make_logout_request("https://untrusted.example"),
                Response(),
                db,
            )

        self.assertEqual(raised.exception.status_code, 403)


if __name__ == "__main__":
    unittest.main()
