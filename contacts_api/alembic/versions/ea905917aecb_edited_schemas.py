"""Edited schemas

Revision ID: ea905917aecb
Revises: d717efb17cd7
Create Date: 2024-07-04 11:22:36.764531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea905917aecb'
down_revision: Union[str, None] = 'd717efb17cd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
