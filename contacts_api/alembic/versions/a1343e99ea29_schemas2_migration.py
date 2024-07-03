"""schemas2 migration

Revision ID: a1343e99ea29
Revises: 5d69040a0f83
Create Date: 2024-07-02 12:04:06.385927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1343e99ea29'
down_revision: Union[str, None] = '5d69040a0f83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
