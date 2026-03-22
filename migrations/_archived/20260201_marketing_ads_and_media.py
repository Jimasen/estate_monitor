from alembic import op
import sqlalchemy as sa


revision = "20260201_marketing"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "recommendation_blocks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("image_url", sa.String(500)),
        sa.Column("link_url", sa.String(500)),
        sa.Column("position", sa.String(50)),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "property_ads",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("price", sa.String(100)),
        sa.Column("location", sa.String(255)),
        sa.Column("description", sa.Text),
        sa.Column("images", sa.JSON),
        sa.Column("contact_phone", sa.String(50)),
        sa.Column("whatsapp_link", sa.String(255)),
        sa.Column("facebook_link", sa.String(255)),
        sa.Column("is_featured", sa.Boolean, default=False),
        sa.Column("is_approved", sa.Boolean, default=False),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "carousel_ads",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("image_url", sa.String(500), nullable=False),
        sa.Column("headline", sa.String(255)),
        sa.Column("sub_text", sa.String(255)),
        sa.Column("link_url", sa.String(500)),
        sa.Column("display_order", sa.Integer, default=0),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "user_media",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("image_url", sa.String(500), nullable=False),
        sa.Column("purpose", sa.String(50)),
        sa.Column("is_approved", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("user_media")
    op.drop_table("carousel_ads")
    op.drop_table("property_ads")
    op.drop_table("recommendation_blocks")
