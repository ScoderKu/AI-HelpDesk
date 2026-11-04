import asyncio
from datetime import datetime, timezone
import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")
os.environ.setdefault("MYSQL_DATABASE", "test")

from fastapi import HTTPException
from starlette.requests import Request
from pydantic import ValidationError
from sqlalchemy.dialects import mysql

from app import main
from app.models import Conversation, Message, Ticket, User
from app.schemas import (
    TicketCreateRequest,
    TicketPriority,
    TicketStatus,
    TicketUpdateRequest,
)


def make_ticket(
    *,
    ticket_id: int = 10,
    user_id: int = 7,
    status: str = "OPEN",
) -> Ticket:
    now = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc).replace(tzinfo=None)
    return Ticket(
        id=ticket_id,
        user_id=user_id,
        conversation_id=None,
        title="Network issue",
        description="Cannot connect to Wi-Fi.",
        status=status,
        priority="MEDIUM",
        created_at=now,
        updated_at=now,
        closed_at=None,
    )


def compile_mysql(statement: object) -> str:
    return str(
        statement.compile(
            dialect=mysql.dialect(),
            compile_kwargs={"literal_binds": True},
        )
    )


class TicketSchemaTests(unittest.TestCase):
    def test_create_defaults_priority_and_forbids_server_owned_fields(self) -> None:
        request = TicketCreateRequest(
            title=" Network issue ",
            description=" Cannot connect to Wi-Fi. ",
        )

        self.assertEqual(request.title, "Network issue")
        self.assertEqual(request.description, "Cannot connect to Wi-Fi.")
        self.assertEqual(request.priority, TicketPriority.MEDIUM)
        with self.assertRaises(ValidationError):
            TicketCreateRequest(
                title="Network issue",
                description="Description",
                user_id=999,
            )
        with self.assertRaises(ValidationError):
            TicketCreateRequest(
                title="Network issue",
                description="Description",
                status="CLOSED",
            )

    def test_create_rejects_blank_text_invalid_priority_and_text_over_mysql_limit(self) -> None:
        with self.assertRaises(ValidationError):
            TicketCreateRequest(title="   ", description="Description")
        with self.assertRaises(ValidationError):
            TicketCreateRequest(title="Valid", description="   ")
        with self.assertRaises(ValidationError):
            TicketCreateRequest(
                title="Valid",
                description="Description",
                priority="URGENT",
            )
        with self.assertRaises(ValidationError):
            TicketCreateRequest(title="Valid", description="é" * 32_768)

    def test_patch_requires_allowed_non_null_fields(self) -> None:
        with self.assertRaises(ValidationError):
            TicketUpdateRequest()
        with self.assertRaises(ValidationError):
            TicketUpdateRequest(title=None)
        with self.assertRaises(ValidationError):
            TicketUpdateRequest(status="CLOSED")
        self.assertEqual(
            TicketUpdateRequest(priority=TicketPriority.HIGH).priority,
            TicketPriority.HIGH,
        )


class TicketEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User(id=7)

    def test_all_ticket_endpoints_require_authenticated_user(self) -> None:
        protected_paths = {
            ("GET", "/api/v1/tickets"),
            ("POST", "/api/v1/tickets"),
            ("POST", "/api/v1/conversations/{conversation_id}/ticket-draft"),
            ("POST", "/api/v1/conversations/{conversation_id}/tickets"),
            ("GET", "/api/v1/tickets/summary"),
            ("GET", "/api/v1/tickets/{ticket_id}"),
            ("PATCH", "/api/v1/tickets/{ticket_id}"),
            ("POST", "/api/v1/tickets/{ticket_id}/close"),
        }
        for route in main.app.routes:
            if not isinstance(route, main.app.router.route_class):
                continue
            for method in route.methods or ():
                if (method, route.path) in protected_paths:
                    dependency_calls = {
                        dependency.call for dependency in route.dependant.dependencies
                    }
                    self.assertIn(main.get_authenticated_user, dependency_calls)
                    protected_paths.remove((method, route.path))

        self.assertFalse(protected_paths)

    def test_list_returns_only_authenticated_users_tickets_in_newest_order(self) -> None:
        own_ticket = make_ticket(user_id=self.user.id)
        db = MagicMock()
        db.scalars.return_value.all.return_value = [own_ticket]

        response = main.list_tickets(self.user, db)

        self.assertEqual([ticket.id for ticket in response], [own_ticket.id])
        statement = compile_mysql(db.scalars.call_args.args[0])
        self.assertIn("tickets.user_id = 7", statement)
        self.assertIn("tickets.created_at DESC, tickets.id DESC", statement)

    def test_summary_counts_only_open_and_closed_tickets_for_user(self) -> None:
        db = MagicMock()
        db.execute.return_value.one.return_value = (4, 3, 1)

        response = main.get_ticket_summary(self.user, db)

        self.assertEqual(response.model_dump(), {"total": 4, "open": 3, "closed": 1})
        statement = compile_mysql(db.execute.call_args.args[0])
        self.assertIn("tickets.user_id = 7", statement)
        self.assertIn("tickets.status = 'OPEN'", statement)
        self.assertIn("tickets.status = 'CLOSED'", statement)

    def test_summary_returns_zero_counts_for_user_without_tickets(self) -> None:
        db = MagicMock()
        db.execute.return_value.one.return_value = (0, None, None)

        response = main.get_ticket_summary(self.user, db)

        self.assertEqual(response.model_dump(), {"total": 0, "open": 0, "closed": 0})

    def test_create_derives_owner_and_defaults_on_server(self) -> None:
        db = MagicMock()
        db.refresh.side_effect = lambda ticket: setattr(ticket, "id", 101)
        request = TicketCreateRequest(
            title="Network issue",
            description="Cannot connect to Wi-Fi.",
        )

        response = main.create_ticket(request, self.user, db)

        created = db.add.call_args.args[0]
        self.assertEqual(created.user_id, self.user.id)
        self.assertEqual(created.status, TicketStatus.OPEN.value)
        self.assertEqual(created.priority, TicketPriority.MEDIUM.value)
        self.assertIsNone(created.conversation_id)
        self.assertEqual(response.id, 101)
        self.assertEqual(response.status, TicketStatus.OPEN)
        self.assertTrue(response.model_dump_json().endswith('Z"}'))
        db.commit.assert_called_once_with()


    def test_ticket_draft_endpoint_returns_model_generated_fields(self) -> None:
        conversation = Conversation(id=55, user_id=self.user.id, response_language="English")
        messages = [
            Message(id=1, conversation_id=55, role="USER", content="My Wi-Fi disconnects every few minutes."),
            Message(id=2, conversation_id=55, role="ASSISTANT", content="Have you restarted the router?"),
            Message(id=3, conversation_id=55, role="USER", content="Yes, and it still disconnects."),
        ]
        db = MagicMock()
        db.scalar.return_value = conversation
        db.scalars.return_value.all.return_value = messages
        request = Request({
            "type": "http", "method": "POST", "path": "/",
            "headers": [(b"origin", b"http://localhost:5173")],
            "query_string": b"", "server": ("localhost", 80),
            "client": ("test", 1234), "scheme": "http",
        })
        generated = SimpleNamespace(
            title="Wi-Fi connection drops repeatedly",
            description="The user's Wi-Fi disconnects every few minutes despite restarting the router.",
        )
        with patch("app.main.generate_ticket_draft", return_value=generated) as generate:
            response = asyncio.run(main.create_conversation_ticket_draft(request, 55, self.user, db))

        self.assertEqual(response.title, generated.title)
        self.assertEqual(response.description, generated.description)
        self.assertEqual(generate.call_args.args[0], [
            {"role": "user", "content": messages[0].content},
            {"role": "assistant", "content": messages[1].content},
            {"role": "user", "content": messages[2].content},
        ])
        self.assertEqual(generate.call_args.args[1], "English")

    def test_create_ticket_from_owned_conversation_links_ticket_and_uses_server_owner(self) -> None:
        from app.models import Conversation

        conversation = Conversation(id=55, user_id=self.user.id)
        db = MagicMock()
        db.scalar.return_value = conversation
        db.refresh.side_effect = lambda ticket: setattr(ticket, "id", 202)
        request = TicketCreateRequest(
            title="Network keeps disconnecting",
            description="The Wi-Fi disconnects after a few minutes.",
            priority="HIGH",
        )

        response = main.create_ticket_from_conversation(request, 55, self.user, db)

        created = db.add.call_args.args[0]
        self.assertEqual(created.user_id, self.user.id)
        self.assertEqual(created.conversation_id, conversation.id)
        self.assertEqual(created.status, TicketStatus.OPEN.value)
        self.assertEqual(created.priority, TicketPriority.HIGH.value)
        self.assertEqual(response.id, 202)
        self.assertEqual(response.status, TicketStatus.OPEN)
        statement = compile_mysql(db.scalar.call_args.args[0])
        self.assertIn("conversations.id = 55", statement)
        self.assertIn("conversations.user_id = 7", statement)
        db.commit.assert_called_once_with()

    def test_create_ticket_from_missing_or_foreign_conversation_returns_404(self) -> None:
        db = MagicMock()
        db.scalar.return_value = None
        request = TicketCreateRequest(title="Network issue", description="Wi-Fi is unavailable.")

        with self.assertRaises(HTTPException) as raised:
            main.create_ticket_from_conversation(request, 999, self.user, db)

        self.assertEqual(raised.exception.status_code, 404)
        db.add.assert_not_called()
        db.commit.assert_not_called()

    def test_get_ticket_filters_by_owner_and_hides_foreign_ticket(self) -> None:
        db = MagicMock()
        db.scalar.return_value = None

        with self.assertRaises(HTTPException) as raised:
            main.get_ticket(10, self.user, db)

        self.assertEqual(raised.exception.status_code, 404)
        statement = compile_mysql(db.scalar.call_args.args[0])
        self.assertIn("tickets.user_id = 7", statement)
        self.assertIn("tickets.id = 10", statement)

    def test_get_ticket_returns_owned_ticket(self) -> None:
        ticket = make_ticket(user_id=self.user.id)
        db = MagicMock()
        db.scalar.return_value = ticket

        response = main.get_ticket(ticket.id, self.user, db)

        self.assertEqual(response.id, ticket.id)
        self.assertEqual(response.title, ticket.title)

    def test_update_changes_only_allowed_fields_on_open_owned_ticket(self) -> None:
        ticket = make_ticket(user_id=self.user.id)
        db = MagicMock()
        db.scalar.return_value = ticket

        response = main.update_ticket(
            TicketUpdateRequest(title="Updated title", priority="HIGH"),
            ticket.id,
            self.user,
            db,
        )

        self.assertEqual(ticket.title, "Updated title")
        self.assertEqual(ticket.priority, "HIGH")
        self.assertEqual(ticket.user_id, self.user.id)
        self.assertEqual(response.title, "Updated title")
        db.commit.assert_called_once_with()
        statement = compile_mysql(db.scalar.call_args.args[0])
        self.assertIn("tickets.user_id = 7", statement)

    def test_update_hides_foreign_ticket(self) -> None:
        db = MagicMock()
        db.scalar.return_value = None

        with self.assertRaises(HTTPException) as raised:
            main.update_ticket(TicketUpdateRequest(title="Changed"), 10, self.user, db)

        self.assertEqual(raised.exception.status_code, 404)
        db.commit.assert_not_called()

    def test_closed_ticket_cannot_be_updated(self) -> None:
        ticket = make_ticket(user_id=self.user.id, status="CLOSED")
        db = MagicMock()
        db.scalar.return_value = ticket

        with self.assertRaises(HTTPException) as raised:
            main.update_ticket(TicketUpdateRequest(title="Changed"), 10, self.user, db)

        self.assertEqual(raised.exception.status_code, 409)
        db.commit.assert_not_called()

    def test_close_marks_owned_ticket_closed_and_sets_timestamps(self) -> None:
        ticket = make_ticket(user_id=self.user.id)
        db = MagicMock()
        db.scalar.return_value = ticket

        response = main.close_ticket(ticket.id, self.user, db)

        self.assertEqual(ticket.status, TicketStatus.CLOSED.value)
        self.assertIsNotNone(ticket.closed_at)
        self.assertEqual(ticket.closed_at, ticket.updated_at)
        self.assertEqual(response.status, TicketStatus.CLOSED)
        db.commit.assert_called_once_with()
        db.refresh.assert_called_once_with(ticket)

    def test_close_hides_foreign_ticket_and_rejects_already_closed_ticket(self) -> None:
        db = MagicMock()
        db.scalar.return_value = None
        with self.assertRaises(HTTPException) as missing:
            main.close_ticket(10, self.user, db)
        self.assertEqual(missing.exception.status_code, 404)

        db.reset_mock()
        db.scalar.return_value = make_ticket(user_id=self.user.id, status="CLOSED")
        with self.assertRaises(HTTPException) as closed:
            main.close_ticket(10, self.user, db)
        self.assertEqual(closed.exception.status_code, 409)
        db.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
