"""add racks (and optional device rack placement)"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20250905_add_racks"
down_revision = "20250905_devices_role_and_unique"  # make sure this matches your previous head
branch_labels = None
depends_on = None


def upgrade() -> None:
    # racks table
    op.create_table(
        "racks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("site_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("sites.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("u_height", sa.Integer(), nullable=False, server_default="42"),
    )
    op.create_index("ix_racks_site_id", "racks", ["site_id"])
    op.create_unique_constraint("uq_racks_site_name", "racks", ["site_id", "name"])

    # extend devices with rack placement
    with op.batch_alter_table("devices") as batch:
        batch.add_column(sa.Column("rack_id", postgresql.UUID(as_uuid=True),
                                   sa.ForeignKey("racks.id", ondelete="SET NULL"), nullable=True))
        batch.add_column(sa.Column("position_u", sa.Integer(), nullable=True))
        batch.create_index("ix_devices_rack_id", ["rack_id"])


def downgrade() -> None:
    # remove rack placement from devices
    with op.batch_alter_table("devices") as batch:
        batch.drop_index("ix_devices_rack_id")
        batch.drop_column("position_u")
        batch.drop_column("rack_id")

    # drop racks table
    op.drop_constraint("uq_racks_site_name", "racks", type_="unique")
    op.drop_index("ix_racks_site_id", table_name="racks")
    op.drop_table("racks")
