import asyncio
from datetime import datetime
import os
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")
os.environ.setdefault("MYSQL_DATABASE", "test")

from fastapi import HTTPException, Request

from app import main
from app.ai import GeneratedReply
from app.models import Conversation, Message, User


def make_request(origin: str | None) -> Request:
    headers = [] if origin is None else [(b"origin", origin.encode())]
    return Request({"type": "http", "headers": headers})


def make_conversation() -> Conversation:
    now = datetime(2026, 11, 3, 10, 0)
    return Conversation(
        id=12,
        user_id=7,
        title=None,
        response_language=None,
        created_at=now,
        updated_at=now,
    )


def make_user_message(message_id: int = 41) -> Message:
    return Message(
        id=message_id,
        conversation_id=12,
        role="USER",
        content="Help with Wi-Fi",
        created_at=datetime(2026, 11, 3, 10, 0),
    )


class ChatLockLeaseTests(unittest.TestCase):
    def test_assert_owned_renews_the_token_owned_lock(self) -> None:
        lease = main.ChatLockLease("chat:conversation:12", "lease-token")
        with patch.object(main.redis_client, "eval", return_value=1) as renew:
            lease.assert_owned()

        renew.assert_called_once_with(
            main.RENEW_CHAT_LOCK_SCRIPT,
            1,
            "chat:conversation:12",
            "lease-token",
            main.CHAT_LOCK_TTL_SECONDS,
        )

    def test_assert_owned_rejects_a_lock_that_expired_or_was_replaced(self) -> None:
        lease = main.ChatLockLease("chat:conversation:12", "old-token")
        with patch.object(main.redis_client, "eval", return_value=0):
            with self.assertRaises(HTTPException) as raised:
                lease.assert_owned()

        self.assertEqual(raised.exception.status_code, 409)


class ChatEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User(id=7)
        self.request = make_request(main.FRONTEND_ORIGINS[0])

    def test_untrusted_or_missing_origin_is_rejected_before_chat_work(self) -> None:
        db = MagicMock()
        with patch.object(main.redis_client, "set") as set_lock:
            with self.assertRaises(HTTPException) as raised:
                asyncio.run(
                    main.send_chat_message(
                        main.ChatMessageRequest(content="Help"),
                        make_request("https://attacker.example"),
                        12,
                        self.user,
                        db,
                    )
                )

        self.assertEqual(raised.exception.status_code, 403)
        set_lock.assert_not_called()
        db.scalar.assert_not_called()

        with self.assertRaises(HTTPException) as missing_origin:
            main.require_trusted_origin(make_request(None))
        self.assertEqual(missing_origin.exception.status_code, 403)

    def test_busy_conversation_is_not_written(self) -> None:
        db = MagicMock()
        with patch.object(main.redis_client, "set", return_value=None):
            with self.assertRaises(HTTPException) as raised:
                asyncio.run(
                    main.send_chat_message(
                        main.ChatMessageRequest(content="Help"),
                        self.request,
                        12,
                        self.user,
                        db,
                    )
                )

        self.assertEqual(raised.exception.status_code, 409)
        db.scalar.assert_called_once()

    def test_new_message_is_blocked_while_previous_message_is_unanswered(self) -> None:
        db = MagicMock()
        conversation = make_conversation()
        db.scalar.side_effect = [conversation.id, conversation, make_user_message()]
        with (
            patch.object(main.redis_client, "set", return_value=True),
            patch.object(main.redis_client, "eval", return_value=1),
        ):
            with self.assertRaises(HTTPException) as raised:
                asyncio.run(
                    main.send_chat_message(
                        main.ChatMessageRequest(content="Another question"),
                        self.request,
                        12,
                        self.user,
                        db,
                    )
                )

        self.assertEqual(raised.exception.status_code, 409)
        db.add.assert_not_called()

    def test_db_transaction_is_ended_before_ai_and_assistant_uses_new_session(self) -> None:
        conversation = make_conversation()
        conversation.response_language = "French"
        user_message = make_user_message()
        db = MagicMock()
        db.scalar.side_effect = [conversation.id, conversation, None]
        db.get.return_value = conversation
        db.refresh.side_effect = lambda item: setattr(item, "id", 41)
        db.scalars.return_value.all.return_value = [user_message]
        persistence_db = MagicMock()
        persistence_db.__enter__.return_value = persistence_db
        persistence_db.get.return_value = conversation
        persistence_db.scalar.return_value = user_message
        persistence_db.refresh.side_effect = lambda item: setattr(item, "id", 42)

        async def generate_after_db_release(*_args):
            self.assertEqual(db.rollback.call_count, 2)
            return GeneratedReply("Restart the router.", "Finnish")

        with (
            patch.object(main.redis_client, "set", return_value=True),
            patch.object(main.redis_client, "eval", return_value=1) as release_lock,
            patch.object(main, "SessionLocal", return_value=persistence_db),
            patch.object(
                main.asyncio,
                "to_thread",
                new=AsyncMock(side_effect=generate_after_db_release),
            ) as generate_call,
        ):
            response = asyncio.run(
                main.send_chat_message(
                    main.ChatMessageRequest(content="Help with Wi-Fi"),
                    self.request,
                    12,
                    self.user,
                    db,
                )
            )

        self.assertEqual(response.user_message.id, 41)
        self.assertEqual(response.assistant_message.content, "Restart the router.")
        self.assertEqual(conversation.response_language, "Finnish")
        generate_call.assert_awaited_once_with(
            main.generate_reply,
            [{"role": "user", "content": "Help with Wi-Fi"}],
            "French",
        )
        persistence_db.commit.assert_called_once()
        self.assertEqual(db.rollback.call_count, 2)
        release_calls = [
            call for call in release_lock.call_args_list if call.args[0] == main.RELEASE_CHAT_LOCK_SCRIPT
        ]
        self.assertEqual(len(release_calls), 1)

    def test_failed_ai_response_identifies_saved_message_for_retry(self) -> None:
        conversation = make_conversation()
        user_message = make_user_message()
        db = MagicMock()
        db.scalar.side_effect = [conversation.id, conversation, None]
        db.refresh.side_effect = lambda item: setattr(item, "id", 41)
        db.scalars.return_value.all.return_value = [user_message]

        with (
            patch.object(main.redis_client, "set", return_value=True),
            patch.object(main.redis_client, "eval", return_value=1),
            patch.object(main.asyncio, "to_thread", new=AsyncMock(side_effect=main.OllamaUnavailableError("offline"))),
        ):
            with self.assertRaises(HTTPException) as raised:
                asyncio.run(
                    main.send_chat_message(
                        main.ChatMessageRequest(content="Help with Wi-Fi"),
                        self.request,
                        12,
                        self.user,
                        db,
                    )
                )

        self.assertEqual(raised.exception.status_code, 503)
        self.assertEqual(raised.exception.headers["X-Chat-Message-Saved"], "true")
        self.assertEqual(raised.exception.headers["X-Chat-Message-Id"], "41")
        self.assertEqual(db.rollback.call_count, 2)

    def test_retry_uses_existing_unanswered_message_without_inserting_another(self) -> None:
        conversation = make_conversation()
        user_message = make_user_message()
        db = MagicMock()
        db.scalar.side_effect = [
            conversation.id,
            conversation,
            user_message,
            user_message,
        ]
        db.get.return_value = conversation
        db.scalars.return_value.all.return_value = [user_message]
        persistence_db = MagicMock()
        persistence_db.__enter__.return_value = persistence_db
        persistence_db.get.return_value = conversation
        persistence_db.scalar.return_value = user_message
        persistence_db.refresh.side_effect = lambda item: setattr(item, "id", 42)

        with (
            patch.object(main.redis_client, "set", return_value=True),
            patch.object(main.redis_client, "eval", return_value=1),
            patch.object(main, "SessionLocal", return_value=persistence_db),
            patch.object(main.asyncio, "to_thread", new=AsyncMock(return_value=GeneratedReply("Restart the router.", None))),
        ):
            response = asyncio.run(
                main.retry_chat_message(
                    self.request,
                    12,
                    41,
                    self.user,
                    db,
                )
            )

        self.assertEqual(response.user_message.id, 41)
        self.assertEqual(response.assistant_message.id, 42)
        self.assertEqual(db.add.call_count, 0)
        persistence_db.add.assert_called_once()
        self.assertEqual(db.rollback.call_count, 2)
