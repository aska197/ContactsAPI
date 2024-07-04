"""Add hashed_password column to users

Revision ID: 9952369324e0
Revises: ea905917aecb
Create Date: 2024-07-04 11:26:14.038438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9952369324e0'
down_revision: Union[str, None] = 'ea905917aecb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
