import os
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")
os.environ.setdefault("MYSQL_DATABASE", "test")

from app import admin


class AdminPasswordResetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.user = MagicMock()
        self.user.id = 17
        self.db = MagicMock()
        self.db.scalar.return_value = self.user

    @patch("app.admin.SessionLocal")
    @patch("app.admin.hash_password", return_value="hashed-temporary-password")
    @patch("app.admin.secrets.token_urlsafe", return_value="temporary-password-123")
    def test_reset_hashes_temporary_password_flags_user_and_revokes_sessions(
        self, token: MagicMock, hash_value: MagicMock, session_local: MagicMock
    ) -> None:
        session_local.return_value = self.db
        result = admin.reset_password(" User@Example.com ")

        self.assertEqual(result, "temporary-password-123")
        self.assertEqual(self.user.password_hash, "hashed-temporary-password")
        self.assertTrue(self.user.must_change_password)
        hash_value.assert_called_once_with("temporary-password-123")
        token.assert_called_once_with(18)
        self.db.execute.assert_called_once()
        self.db.commit.assert_called_once_with()
        self.db.rollback.assert_not_called()
        self.db.close.assert_called_once_with()

    @patch("app.admin.SessionLocal")
    @patch("app.admin.secrets.token_urlsafe", return_value="temporary-password-123")
    def test_unknown_user_rolls_back_without_returning_temporary_password(
        self, _token: MagicMock, session_local: MagicMock
    ) -> None:
        self.db.scalar.return_value = None
        session_local.return_value = self.db

        with self.assertRaises(LookupError):
            admin.reset_password("missing@example.com")

        self.db.commit.assert_not_called()
        self.db.rollback.assert_called_once_with()
        self.db.close.assert_called_once_with()

    @patch("app.admin.SessionLocal")
    @patch("app.admin.secrets.token_urlsafe", return_value="temporary-password-123")
    def test_database_failure_rolls_back(
        self, _token: MagicMock, session_local: MagicMock
    ) -> None:
        self.db.commit.side_effect = RuntimeError("database unavailable")
        session_local.return_value = self.db

        with self.assertRaises(RuntimeError):
            admin.reset_password("user@example.com")

        self.db.rollback.assert_called_once_with()
        self.db.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
