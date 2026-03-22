"""marketing ads and media

Revision ID: cc1e8ad1a023
Revises: 313a30589b22
Create Date: 2026-02-03 00:14:03.990073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc1e8ad1a023'
down_revision: Union[str, Sequence[str], None] = '313a30589b22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
