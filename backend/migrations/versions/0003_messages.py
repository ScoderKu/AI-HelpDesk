"""Create or adopt persistent conversation messages.

Revision ID: 0003_messages
Revises: 0002_conversations_and_tickets
Create Date: 2026-11-02
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "0003_messages"
down_revision = "0002_conversations_and_tickets"
branch_labels = None
depends_on = None


def upgrade() -> None:
    inspector = inspect(op.get_bind())
    if "messages" not in inspector.get_table_names():
        op.create_table(
            "messages",
            sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column("conversation_id", sa.BigInteger(), nullable=False),
            sa.Column("role", sa.String(length=20), nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(
                ["conversation_id"], ["conversations.id"], ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        inspector = inspect(op.get_bind())

    columns = {column["name"]: column for column in inspector.get_columns("messages")}
    expected = {
        "id": (sa.BigInteger, False),
        "conversation_id": (sa.BigInteger, False),
        "role": (sa.String, False),
        "content": (sa.Text, False),
        "created_at": (sa.DateTime, False),
    }
    for name, (expected_type, nullable) in expected.items():
        column = columns.get(name)
        if column is None or not isinstance(column["type"], expected_type):
            raise RuntimeError(f"Existing messages table has an incompatible {name} column.")
        if column["nullable"] != nullable:
            raise RuntimeError(f"Existing messages.{name} has incompatible nullability.")

    if inspector.get_pk_constraint("messages").get("constrained_columns") != ["id"]:
        raise RuntimeError("Existing messages table must use id as its primary key.")

    foreign_keys = inspector.get_foreign_keys("messages")
    if not any(
        foreign_key.get("constrained_columns") == ["conversation_id"]
        and foreign_key.get("referred_table") == "conversations"
        and foreign_key.get("referred_columns") == ["id"]
        for foreign_key in foreign_keys
    ):
        raise RuntimeError("Existing messages.conversation_id must reference conversations.id.")

    role_length = columns["role"]["type"].length
    if role_length == 100:
        max_role_length = op.get_bind().execute(
            sa.text("SELECT MAX(CHAR_LENGTH(role)) FROM messages")
        ).scalar_one()
        if max_role_length is not None and max_role_length > 20:
            raise RuntimeError("Existing messages.role contains values longer than 20 characters.")
        op.alter_column(
            "messages",
            "role",
            existing_type=sa.String(length=100),
            type_=sa.String(length=20),
            existing_nullable=False,
            nullable=False,
        )
    elif role_length != 20:
        raise RuntimeError("Existing messages.role must be VARCHAR(20) or VARCHAR(100).")

    indexes = inspector.get_indexes("messages")
    if not any(
        index.get("column_names") == ["conversation_id", "created_at", "id"]
        for index in indexes
    ):
        op.create_index(
            "ix_messages_conversation_created_id",
            "messages",
            ["conversation_id", "created_at", "id"],
        )


def downgrade() -> None:
    raise RuntimeError(
        "The messages table may contain data that predates this migration. "
        "It cannot be downgraded automatically without risking chat history."
    )
