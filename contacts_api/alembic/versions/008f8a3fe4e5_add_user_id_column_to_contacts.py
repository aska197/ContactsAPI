"""Add user_id column to contacts

Revision ID: 008f8a3fe4e5
Revises: 1ef0e599d3e6
Create Date: 2024-06-18 11:02:32.439842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '008f8a3fe4e5'
down_revision: Union[str, None] = '1ef0e599d3e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
