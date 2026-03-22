"""add_is_approved_to_ads_and_media

Revision ID: add_is_approved_202602
Revises: 4cc713694ffa
Create Date: 2026-02-03 12:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_is_approved_202602'
down_revision = '4cc713694ffa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_approved column to property_ads
    op.add_column(
        'property_ads',
        sa.Column('is_approved', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false())
    )

    # Add is_approved column to user_media
    op.add_column(
        'user_media',
        sa.Column('is_approved', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false())
    )


def downgrade() -> None:
    op.drop_column('property_ads', 'is_approved')
    op.drop_column('user_media', 'is_approved')
