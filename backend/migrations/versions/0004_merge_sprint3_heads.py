"""Merge the message and forced-password migration branches.

Revision ID: 0004_merge_sprint3_heads
Revises: 0003_messages, 0003_must_change_password
"""

revision = "0004_merge_sprint3_heads"
down_revision = ("0003_messages", "0003_must_change_password")
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
