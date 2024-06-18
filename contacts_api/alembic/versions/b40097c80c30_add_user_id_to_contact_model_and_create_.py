"""Add user_id to Contact model and create relationships

Revision ID: b40097c80c30
Revises: 724867b39dac
Create Date: 2024-06-18 00:00:15.533608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b40097c80c30'
down_revision: Union[str, None] = '724867b39dac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
