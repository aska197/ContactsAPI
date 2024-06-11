"""fixing

Revision ID: 724867b39dac
Revises: 9f995d946077
Create Date: 2024-06-11 18:43:48.915505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '724867b39dac'
down_revision: Union[str, None] = '9f995d946077'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
