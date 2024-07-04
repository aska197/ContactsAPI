"""Add hashed_password to users

Revision ID: d717efb17cd7
Revises: 4697b1bf8148
Create Date: 2024-07-04 11:17:24.871116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd717efb17cd7'
down_revision: Union[str, None] = '4697b1bf8148'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
