import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

from sqlalchemy.dialects import mysql

os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")
os.environ.setdefault("MYSQL_DATABASE", "test")

from app import main


class CleanupExpiredSessionsTests(TestCase):
    def test_deletes_expired_sessions_by_primary_key_in_separate_batches(self) -> None:
        db = MagicMock()
        db.__enter__.return_value = db
        db.scalars.return_value.all.side_effect = [["expired-session"], []]

        with patch.object(main, "SessionLocal", return_value=db):
            main.cleanup_expired_sessions()

        self.assertEqual(db.execute.call_count, 1)
        statement = db.execute.call_args.args[0]
        sql = str(
            statement.compile(
                dialect=mysql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        )
        self.assertIn("auth_sessions.id IN ('expired-session')", sql)
        self.assertNotIn("expires_at", sql)
        db.commit.assert_called_once_with()


if __name__ == "__main__":
    import unittest

    unittest.main()
