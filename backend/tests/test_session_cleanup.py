import os
from datetime import datetime
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


class DataRetentionCleanupTests(TestCase):
    def test_retention_cutoff_uses_three_calendar_months(self) -> None:
        self.assertEqual(
            main.data_retention_cutoff(datetime(2025, 5, 31, 12, 30)),
            datetime(2025, 2, 28, 12, 30),
        )
        self.assertEqual(
            main.data_retention_cutoff(datetime(2024, 5, 31, 12, 30)),
            datetime(2024, 2, 29, 12, 30),
        )

    def test_deletes_expired_closed_tickets_and_unlinked_inactive_conversations(
        self,
    ) -> None:
        db = MagicMock()
        db.__enter__.return_value = db
        db.scalars.return_value.all.side_effect = [
            [11, 12],
            [],
            [21],
            [],
        ]
        cutoff = datetime(2025, 2, 28, 12, 30)

        with (
            patch.object(main, "SessionLocal", return_value=db),
            patch.object(main, "data_retention_cutoff", return_value=cutoff),
        ):
            main.cleanup_retained_data()

        self.assertEqual(db.execute.call_count, 2)
        ticket_select = str(
            db.scalars.call_args_list[0].args[0].compile(
                dialect=mysql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        )
        ticket_delete = str(
            db.execute.call_args_list[0].args[0].compile(
                dialect=mysql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        )
        conversation_select = str(
            db.scalars.call_args_list[2].args[0].compile(
                dialect=mysql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        )
        conversation_delete = str(
            db.execute.call_args_list[1].args[0].compile(
                dialect=mysql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        )
        self.assertIn("tickets.status = 'CLOSED'", ticket_select)
        self.assertIn("tickets.closed_at <= '2025-02-28 12:30:00'", ticket_select)
        self.assertIn("tickets.id IN (11, 12)", ticket_delete)
        self.assertIn("tickets.status = 'CLOSED'", ticket_delete)
        self.assertIn("tickets.closed_at <= '2025-02-28 12:30:00'", ticket_delete)
        self.assertIn(
            "conversations.updated_at <= '2025-02-28 12:30:00'",
            conversation_select,
        )
        self.assertIn("conversations.id IN (21)", conversation_delete)
        self.assertIn(
            "conversations.updated_at <= '2025-02-28 12:30:00'",
            conversation_delete,
        )
        self.assertIn("NOT (EXISTS", conversation_delete)
        self.assertIn("tickets.status != 'CLOSED'", conversation_delete)
        self.assertIn("tickets.closed_at IS NULL", conversation_delete)
        self.assertIn(
            "tickets.closed_at > '2025-02-28 12:30:00'",
            conversation_delete,
        )
        self.assertEqual(db.commit.call_count, 2)

if __name__ == "__main__":
    import unittest

    unittest.main()
