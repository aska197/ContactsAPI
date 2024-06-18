"""Add user_id column to contacts

Revision ID: 1ef0e599d3e6
Revises: b40097c80c30
Create Date: 2024-06-18 11:01:22.704854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ef0e599d3e6'
down_revision: Union[str, None] = 'b40097c80c30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
