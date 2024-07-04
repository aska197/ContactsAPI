"""Add hashed_password to users

Revision ID: 4697b1bf8148
Revises: a1343e99ea29
Create Date: 2024-07-04 11:11:56.000745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4697b1bf8148'
down_revision: Union[str, None] = 'a1343e99ea29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))

def downgrade():
    op.drop_column('users', 'hashed_password')
