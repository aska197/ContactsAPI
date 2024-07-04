"""Remove hashed_password column from users

Revision ID: df0643c5de2a
Revises: 9952369324e0
Create Date: 2024-07-04 11:29:56.917091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df0643c5de2a'
down_revision: Union[str, None] = '9952369324e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
