"""Create the initial users and authentication-session schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-10-31
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adopt databases created by the previous metadata.create_all startup path.
    existing_tables = set(inspect(op.get_bind()).get_table_names())

    if "users" not in existing_tables:
        op.create_table(
            "users",
            sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column("first_name", sa.String(length=100), nullable=False),
            sa.Column("last_name", sa.String(length=100), nullable=False),
            sa.Column("username", sa.String(length=100), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("password_hash", sa.String(length=255), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"),
            sa.UniqueConstraint("username"),
        )

    if "auth_sessions" not in existing_tables:
        op.create_table(
            "auth_sessions",
            sa.Column("id", sa.String(length=32), nullable=False),
            sa.Column("user_id", sa.BigInteger(), nullable=False),
            sa.Column("expires_at", sa.DateTime(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_auth_sessions_user_id", "auth_sessions", ["user_id"])
        op.create_index(
            "ix_auth_sessions_expires_at", "auth_sessions", ["expires_at"]
        )


def downgrade() -> None:
    raise RuntimeError(
        "The initial schema revision is a non-destructive baseline and cannot "
        "be downgraded automatically. Back up the database and handle schema "
        "removal explicitly if it is required."
    )
