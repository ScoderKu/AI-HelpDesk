"""Add the forced password-change flag for administrator resets.

Revision ID: 0003_must_change_password
Revises: 0002_conversations_and_tickets
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "0003_must_change_password"
down_revision = "0002_conversations_and_tickets"
branch_labels = None
depends_on = None


def upgrade() -> None:
    columns = {column["name"] for column in inspect(op.get_bind()).get_columns("users")}
    if "must_change_password" not in columns:
        op.add_column(
            "users",
            sa.Column(
                "must_change_password",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        )
        op.alter_column("users", "must_change_password", server_default=None)


def downgrade() -> None:
    columns = {column["name"] for column in inspect(op.get_bind()).get_columns("users")}
    if "must_change_password" in columns:
        op.drop_column("users", "must_change_password")
