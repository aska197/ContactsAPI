"""schemas migration

Revision ID: 5d69040a0f83
Revises: 008f8a3fe4e5
Create Date: 2024-07-02 11:56:42.743090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d69040a0f83'
down_revision: Union[str, None] = '008f8a3fe4e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
