"""Persist an explicit AI response-language preference per conversation.

Revision ID: 0006_response_language
Revises: 0005_data_retention_indexes
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "0006_response_language"
down_revision = "0005_data_retention_indexes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    columns = {
        column["name"]
        for column in inspect(op.get_bind()).get_columns("conversations")
    }
    if "response_language" not in columns:
        op.add_column(
            "conversations",
            sa.Column("response_language", sa.String(length=100), nullable=True),
        )


def downgrade() -> None:
    columns = {
        column["name"]
        for column in inspect(op.get_bind()).get_columns("conversations")
    }
    if "response_language" in columns:
        op.drop_column("conversations", "response_language")
