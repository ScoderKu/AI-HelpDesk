"""Adopt the conversation table and add the ticket schema/indexes.

Revision ID: 0002_conversations_and_tickets
Revises: 0001_initial_schema
Create Date: 2026-11-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "0002_conversations_and_tickets"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def _validate_columns(
    table_name: str,
    expected: dict[str, tuple[type[sa.types.TypeEngine], bool]],
) -> None:
    inspector = inspect(op.get_bind())
    columns = {column["name"]: column for column in inspector.get_columns(table_name)}
    for name, (expected_type, nullable) in expected.items():
        column = columns.get(name)
        if column is None:
            raise RuntimeError(
                f"Existing {table_name} table is missing required column {name!r}."
            )
        if not isinstance(column["type"], expected_type):
            raise RuntimeError(
                f"Existing {table_name}.{name} has incompatible type "
                f"{column['type']!s}."
            )
        if column["nullable"] != nullable:
            raise RuntimeError(
                f"Existing {table_name}.{name} has incompatible nullability."
            )


def _validate_primary_key(table_name: str) -> None:
    primary_key = inspect(op.get_bind()).get_pk_constraint(table_name)
    if primary_key.get("constrained_columns") != ["id"]:
        raise RuntimeError(
            f"Existing {table_name} table must use id as its primary key."
        )


def _validate_foreign_key(
    table_name: str,
    column_name: str,
    referred_table: str,
    referred_column: str = "id",
) -> None:
    foreign_keys = inspect(op.get_bind()).get_foreign_keys(table_name)
    if not any(
        foreign_key.get("constrained_columns") == [column_name]
        and foreign_key.get("referred_table") == referred_table
        and foreign_key.get("referred_columns") == [referred_column]
        for foreign_key in foreign_keys
    ):
        raise RuntimeError(
            f"Existing {table_name}.{column_name} must reference "
            f"{referred_table}.{referred_column}."
        )


def _ensure_index(table_name: str, name: str, columns: list[str]) -> None:
    indexes = inspect(op.get_bind()).get_indexes(table_name)
    if any(index.get("column_names") == columns for index in indexes):
        return
    op.create_index(name, table_name, columns)


def _create_conversations() -> None:
    op.create_table(
        "conversations",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def _adopt_conversations() -> None:
    _validate_columns(
        "conversations",
        {
            "id": (sa.BigInteger, False),
            "user_id": (sa.BigInteger, False),
            "title": (sa.String, True),
            "created_at": (sa.DateTime, False),
            "updated_at": (sa.DateTime, False),
        },
    )
    _validate_primary_key("conversations")
    _validate_foreign_key("conversations", "user_id", "users")

    title = next(
        column
        for column in inspect(op.get_bind()).get_columns("conversations")
        if column["name"] == "title"
    )
    title_length = title["type"].length
    if title_length == 100:
        op.alter_column(
            "conversations",
            "title",
            existing_type=sa.String(length=100),
            type_=sa.String(length=200),
            existing_nullable=True,
            nullable=True,
        )
    elif title_length != 200:
        raise RuntimeError(
            "Existing conversations.title must be VARCHAR(100) or VARCHAR(200)."
        )


def _create_tickets() -> None:
    op.create_table(
        "tickets",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("conversation_id", sa.BigInteger(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["conversation_id"], ["conversations.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def _adopt_tickets() -> None:
    _validate_columns(
        "tickets",
        {
            "id": (sa.BigInteger, False),
            "user_id": (sa.BigInteger, False),
            "conversation_id": (sa.BigInteger, True),
            "title": (sa.String, False),
            "description": (sa.Text, False),
            "status": (sa.String, False),
            "priority": (sa.String, False),
            "created_at": (sa.DateTime, False),
            "updated_at": (sa.DateTime, False),
            "closed_at": (sa.DateTime, True),
        },
    )
    _validate_primary_key("tickets")
    _validate_foreign_key("tickets", "user_id", "users")
    _validate_foreign_key("tickets", "conversation_id", "conversations")

    inspector = inspect(op.get_bind())
    expected_lengths = {"title": 200, "status": 20, "priority": 20}
    for name, length in expected_lengths.items():
        column = next(
            item for item in inspector.get_columns("tickets") if item["name"] == name
        )
        if column["type"].length != length:
            raise RuntimeError(
                f"Existing tickets.{name} must be VARCHAR({length})."
            )


def upgrade() -> None:
    inspector = inspect(op.get_bind())
    if "conversations" not in inspector.get_table_names():
        _create_conversations()
    else:
        _adopt_conversations()
    _ensure_index(
        "conversations",
        "ix_conversations_user_updated_at",
        ["user_id", "updated_at"],
    )

    inspector = inspect(op.get_bind())
    if "tickets" not in inspector.get_table_names():
        _create_tickets()
    else:
        _adopt_tickets()
    _ensure_index("tickets", "ix_tickets_user_created_at", ["user_id", "created_at"])
    _ensure_index("tickets", "ix_tickets_user_status", ["user_id", "status"])
    _ensure_index("tickets", "ix_tickets_conversation_id", ["conversation_id"])


def downgrade() -> None:
    raise RuntimeError(
        "This migration adopts existing tables and may widen conversations.title. "
        "It cannot be downgraded automatically without risking existing data."
    )
