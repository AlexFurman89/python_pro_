"""add birth_date to user

Revision ID: 1f7f44e77107
Revises: 27088205bb83
Create Date: 2025-08-20 17:38:06.064118
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1f7f44e77107"
down_revision: Union[str, Sequence[str], None] = "27088205bb83"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column("user", sa.Column("birth_date", sa.Date(), nullable=True))


    op.add_column("income", sa.Column("date", sa.DateTime(), nullable=True))
    op.add_column("spend", sa.Column("date", sa.DateTime(), nullable=True))


def downgrade() -> None:

    op.drop_column("spend", "date")
    op.drop_column("income", "date")
    op.drop_column("user", "birth_date")