"""add users and note owner foreign key

Revision ID: 12016ddc35f1
Revises: 1e7d494f5830
Create Date: 2026-10-28 19:02:17.389214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12016ddc35f1'
down_revision: Union[str, Sequence[str], None] = '1e7d494f5830'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False, unique=True),
    )
    op.create_foreign_key(
        "fk_notes_user_id_users",
        "notes",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_notes_user_id_users", "notes", type_="foreignkey")
    op.drop_table("users")
