"""merge property_sales migration

Revision ID: 169d524f07dd
Revises: create_property_sales, 587258fd3c9c
Create Date: 2026-03-20 05:54:56.772090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '169d524f07dd'
down_revision: Union[str, Sequence[str], None] = ('create_property_sales', '587258fd3c9c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
