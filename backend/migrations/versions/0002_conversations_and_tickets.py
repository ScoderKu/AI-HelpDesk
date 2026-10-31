"""Add the conversation and ticket tables from the system data model.

Revision ID: 0002_conversations_and_tickets
Revises: 0001_initial_schema
Create Date: 2026-11-01
"""
from alembic import op
import sqlalchemy as sa


revision = "0002_conversations_and_tickets"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
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
    op.create_index(
        "ix_conversations_user_updated_at",
        "conversations",
        ["user_id", "updated_at"],
    )

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
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tickets_user_created_at", "tickets", ["user_id", "created_at"]
    )
    op.create_index(
        "ix_tickets_user_status", "tickets", ["user_id", "status"]
    )
    op.create_index("ix_tickets_conversation_id", "tickets", ["conversation_id"])


def downgrade() -> None:
    op.drop_index("ix_tickets_conversation_id", table_name="tickets")
    op.drop_index("ix_tickets_user_status", table_name="tickets")
    op.drop_index("ix_tickets_user_created_at", table_name="tickets")
    op.drop_table("tickets")
    op.drop_index("ix_conversations_user_updated_at", table_name="conversations")
    op.drop_table("conversations")
