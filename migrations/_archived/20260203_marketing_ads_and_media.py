"""Marketing ads, user media, recommendations, and branding tables

Revision ID: 20260203_marketing_ads_and_media
Revises: 313a30589b22
Create Date: 2026-02-03 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260203_marketing_ads_and_media'
down_revision = '313a30589b22'
branch_labels = None
depends_on = None


def upgrade():
    # ---------------------------
    # Property / Marketing Ads Table
    # ---------------------------
    op.create_table(
        'property_ads',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('image_url', sa.String(512), nullable=True),
        sa.Column('link', sa.String(512), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Optional: full-text index on title + description
    op.create_index(
        'ix_property_ads_fulltext',
        'property_ads',
        ['title', 'description'],
        mysql_prefix='FULLTEXT'
    )

    # ---------------------------
    # User Uploaded Media Table
    # ---------------------------
    op.create_table(
        'user_ad_media',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('image_url', sa.String(512), nullable=False),
        sa.Column('caption', sa.String(255), nullable=True),
        sa.Column('approved', sa.Boolean, nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # ---------------------------
    # Recommendations Table
    # ---------------------------
    op.create_table(
        'recommendations',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # ---------------------------
    # App Settings / Branding Table
    # ---------------------------
    op.create_table(
        'app_settings',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('app_name', sa.String(255), nullable=False, default='Property & Business Management App'),
        sa.Column('primary_color', sa.String(20), nullable=True),
        sa.Column('secondary_color', sa.String(20), nullable=True),
        sa.Column('logo_url', sa.String(512), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('app_settings')
    op.drop_table('recommendations')
    op.drop_index('ix_property_ads_fulltext', table_name='property_ads')
    op.drop_table('user_ad_media')
    op.drop_table('property_ads')
