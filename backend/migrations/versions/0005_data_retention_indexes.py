"""Add indexes used by scheduled data retention cleanup.

Revision ID: 0005_data_retention_indexes
Revises: 0004_merge_sprint3_heads
"""
from alembic import op
from sqlalchemy import inspect


revision = "0005_data_retention_indexes"
down_revision = "0004_merge_sprint3_heads"
branch_labels = None
depends_on = None


def _ensure_index(table_name: str, index_name: str, columns: list[str]) -> None:
    indexes = inspect(op.get_bind()).get_indexes(table_name)
    if any(index.get("column_names") == columns for index in indexes):
        return
    op.create_index(index_name, table_name, columns)


def upgrade() -> None:
    _ensure_index(
        "conversations",
        "ix_conversations_updated_at",
        ["updated_at"],
    )
    _ensure_index(
        "tickets",
        "ix_tickets_status_closed_at",
        ["status", "closed_at"],
    )


def downgrade() -> None:
    indexes = inspect(op.get_bind()).get_indexes("conversations")
    if any(index.get("name") == "ix_conversations_updated_at" for index in indexes):
        op.drop_index("ix_conversations_updated_at", table_name="conversations")

    indexes = inspect(op.get_bind()).get_indexes("tickets")
    if any(index.get("name") == "ix_tickets_status_closed_at" for index in indexes):
        op.drop_index("ix_tickets_status_closed_at", table_name="tickets")
