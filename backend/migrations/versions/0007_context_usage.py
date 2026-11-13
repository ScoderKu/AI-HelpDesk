"""Persist the most recent prompt plus generated-response token count.

Revision ID: 0007_context_usage
Revises: 0006_response_language
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "0007_context_usage"
down_revision = "0006_response_language"
branch_labels = None
depends_on = None


def upgrade() -> None:
    columns = {
        column["name"]
        for column in inspect(op.get_bind()).get_columns("conversations")
    }
    if "last_context_tokens" not in columns:
        op.add_column("conversations", sa.Column("last_context_tokens", sa.Integer(), nullable=True))


def downgrade() -> None:
    columns = {
        column["name"]
        for column in inspect(op.get_bind()).get_columns("conversations")
    }
    if "last_context_tokens" in columns:
        op.drop_column("conversations", "last_context_tokens")
