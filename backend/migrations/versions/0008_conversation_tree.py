"""Add parent/child conversation lineage and persisted context summaries.

Revision ID: 0008_conversation_tree
Revises: 0007_context_usage
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "0008_conversation_tree"
down_revision = "0007_context_usage"
branch_labels = None
depends_on = None


def upgrade() -> None:
    columns = {
        column["name"]
        for column in inspect(op.get_bind()).get_columns("conversations")
    }
    if "parent_conversation_id" not in columns:
        op.add_column(
            "conversations",
            sa.Column("parent_conversation_id", sa.BigInteger(), nullable=True),
        )
        op.create_foreign_key(
            "fk_conversations_parent_conversation_id",
            "conversations",
            "conversations",
            ["parent_conversation_id"],
            ["id"],
            ondelete="SET NULL",
        )
        op.create_index(
            "ix_conversations_parent_id",
            "conversations",
            ["parent_conversation_id"],
            unique=False,
        )
    if "context_summary" not in columns:
        op.add_column(
            "conversations",
            sa.Column("context_summary", sa.Text(), nullable=True),
        )


def downgrade() -> None:
    columns = {
        column["name"]
        for column in inspect(op.get_bind()).get_columns("conversations")
    }
    if "context_summary" in columns:
        op.drop_column("conversations", "context_summary")
    if "parent_conversation_id" in columns:
        op.drop_index("ix_conversations_parent_id", table_name="conversations")
        op.drop_constraint(
            "fk_conversations_parent_conversation_id",
            "conversations",
            type_="foreignkey",
        )
        op.drop_column("conversations", "parent_conversation_id")
