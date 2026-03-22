"""create property_sales table

Revision ID: create_property_sales
Revises: 
Create Date: 2026-03-20 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "create_property_sales"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "property_sales",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("property_name", sa.String(255), nullable=False),
        sa.Column("property_address", sa.String(255), nullable=False),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("seller_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("buyer_id", sa.Integer, sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("property_sales")
