"""add email and phone_number to tenants safely

Revision ID: add_email_phone_tenants_safe
Revises: <previous_revision_id>
Create Date: 2026-03-19 16:30:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
# --- top of file ---
revision = 'b6b70c87cfde'
down_revision = '8025aaafa2be'
branch_labels = None
depends_on = None
# ----------------------

def upgrade():
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('tenants')]

    if 'email' not in columns:
        op.add_column('tenants', sa.Column('email', sa.String(length=255), nullable=True))
    if 'phone_number' not in columns:
        op.add_column('tenants', sa.Column('phone_number', sa.String(length=20), nullable=True))


def downgrade():
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('tenants')]

    if 'phone_number' in columns:
        op.drop_column('tenants', 'phone_number')
    if 'email' in columns:
        op.drop_column('tenants', 'email')
