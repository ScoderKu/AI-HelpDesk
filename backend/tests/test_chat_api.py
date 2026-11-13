import asyncio
import json
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



    def test_effective_history_combines_all_pending_user_messages(self) -> None:
        answered_user = Message(
            id=10, conversation_id=12, role="USER", content="Earlier question",
            created_at=datetime(2026, 11, 3, 9, 0),
        )
        answered_assistant = Message(
            id=11, conversation_id=12, role="ASSISTANT", content="Earlier answer",
            created_at=datetime(2026, 11, 3, 9, 1),
        )
        pending_one = Message(
            id=12, conversation_id=12, role="USER", content="The app crashes",
            created_at=datetime(2026, 11, 3, 9, 2),
        )
        pending_two = Message(
            id=13, conversation_id=12, role="USER", content="It happens after login",
            created_at=datetime(2026, 11, 3, 9, 3),
        )
        db = MagicMock()
        db.scalar.return_value = 11
        db.scalars.side_effect = [
            MagicMock(all=MagicMock(return_value=[pending_one, pending_two])),
            MagicMock(all=MagicMock(return_value=[answered_assistant, answered_user])),
        ]

        messages, effective = main.build_effective_chat_history(db, 12, 13)

        self.assertEqual(effective, "The app crashes\n\nIt happens after login")
        self.assertEqual(messages, [
            {"role": "user", "content": "Earlier question"},
            {"role": "assistant", "content": "Earlier answer"},
            {"role": "user", "content": "The app crashes\n\nIt happens after login"},
        ])

class ChatEndpointTests(unittest.TestCase):

    def test_running_model_context_reads_actual_ollama_context_length(self) -> None:
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps({
            "models": [{"name": main.OLLAMA_MODEL, "context_length": 32768}],
        }).encode("utf-8")
        with patch("urllib.request.urlopen", return_value=response):
            self.assertEqual(main.get_running_model_context(), 32768)

    def test_running_model_context_is_unknown_when_model_is_not_loaded(self) -> None:
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps({"models": []}).encode("utf-8")
        with patch("urllib.request.urlopen", return_value=response):
            self.assertIsNone(main.get_running_model_context())


    def test_generation_control_cancels_and_closes_active_ollama_response(self) -> None:
        control = main.GenerationControl()
        response = MagicMock()
        control.attach_response(response)

        self.assertTrue(control.cancel())
        self.assertTrue(control.cancelled.is_set())
        response.close.assert_called_once()
        self.assertFalse(control.mark_completed())

    def test_generation_control_does_not_cancel_after_completion(self) -> None:
        control = main.GenerationControl()
        self.assertTrue(control.mark_completed())
        self.assertFalse(control.cancel())
        self.assertFalse(control.cancelled.is_set())


    def test_continuation_request_requires_parent_summary_and_title(self) -> None:
        with self.assertRaises(ValueError):
            main.ConversationCreateRequest(parent_conversation_id=12, title="Continuation")
        with self.assertRaises(ValueError):
            main.ConversationCreateRequest(context_summary="Summary without a parent")
        request = main.ConversationCreateRequest(
            parent_conversation_id=12,
            title="Continuation",
            context_summary="  Keep the verified technical context.  ",
        )
        self.assertEqual(request.context_summary, "Keep the verified technical context.")

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

    def test_new_message_can_supplement_an_unanswered_user_message(self) -> None:
        conversation = make_conversation()
        assistant_message = main.MessageResponse(
            id=43,
            role="ASSISTANT",
            content="Combined answer",
            created_at=datetime(2026, 11, 3, 10, 1),
        )
        db = MagicMock()
        db.scalar.side_effect = [conversation.id, conversation]
        db.refresh.side_effect = lambda item: setattr(item, "id", 42)
        with (
            patch.object(main.redis_client, "set", return_value=True),
            patch.object(main.redis_client, "eval", return_value=1),
            patch.object(main, "generate_assistant_for_message", new=AsyncMock(return_value=assistant_message)) as generate,
        ):
            response = asyncio.run(
                main.send_chat_message(
                    main.ChatMessageRequest(content="And the router light is red."),
                    self.request,
                    12,
                    self.user,
                    db,
                )
            )

        self.assertEqual(response.user_message.id, 42)
        self.assertEqual(response.assistant_message.content, "Combined answer")
        db.add.assert_called_once()
        generate.assert_awaited_once()

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
                main,
                "build_knowledge_context",
                return_value=([], "No matching local Knowledge Base source was retrieved.", []),
            ),
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
            "No matching local Knowledge Base source was retrieved.",
            [],
            context_summary=None,
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
