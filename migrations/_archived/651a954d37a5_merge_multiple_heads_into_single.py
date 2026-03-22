"""merge multiple heads into single

Revision ID: 651a954d37a5
Revises: 20260201_marketing, 20260203_marketing_ads_and_media, cc1e8ad1a023
Create Date: 2026-02-03 00:25:53.448912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '651a954d37a5'
down_revision: Union[str, Sequence[str], None] = ('20260201_marketing', '20260203_marketing_ads_and_media', 'cc1e8ad1a023')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
