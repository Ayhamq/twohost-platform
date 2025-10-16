"""add interfaces and cables; link ip_addresses.interface_id -> interfaces.id"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20250906_interfaces_and_cables"
down_revision = "20250905_add_racks"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)

    # 1) interfaces
    if not insp.has_table("interfaces"):
        op.create_table(
            "interfaces",
            sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
            sa.Column(
                "device_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey("devices.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("name", sa.String(length=64), nullable=False),
            sa.Column("type", sa.String(length=32), nullable=False, server_default="ethernet"),
            sa.Column("admin_up", sa.Boolean(), nullable=False, server_default=sa.text("true")),
            sa.Column("oper_up", sa.Boolean(), nullable=False, server_default=sa.text("false")),
            sa.Column("mtu", sa.Integer(), nullable=True),
            sa.Column("mac", postgresql.MACADDR, nullable=True),
            sa.Column("description", sa.String(length=255), nullable=True),
        )
        # unique per-device name
        op.create_unique_constraint("uq_interfaces_device_name", "interfaces", ["device_id", "name"])

    # index on device_id (create only if missing)
    try:
        existing_if_idx = [ix["name"] for ix in insp.get_indexes("interfaces")]
    except Exception:
        existing_if_idx = []
    if "ix_interfaces_device_id" not in existing_if_idx:
        op.create_index("ix_interfaces_device_id", "interfaces", ["device_id"])

    # 2) cables
    if not insp.has_table("cables"):
        op.create_table(
            "cables",
            sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
            sa.Column(
                "a_interface_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey("interfaces.id", ondelete="CASCADE"),
                unique=True,
                nullable=False,
            ),
            sa.Column(
                "b_interface_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey("interfaces.id", ondelete="CASCADE"),
                unique=True,
                nullable=False,
            ),
            sa.Column("label", sa.String(length=64), nullable=True),
            sa.Column("color", sa.String(length=16), nullable=True),
        )
        # make sure ends are distinct (skip if exists)
        try:
            op.create_check_constraint("ck_cable_distinct_ends", "cables", "a_interface_id <> b_interface_id")
        except Exception:
            pass

    # 3) Link ip_addresses.interface_id -> interfaces.id
    # index on interface_id (if missing)
    try:
        existing_ip_idx = [ix["name"] for ix in insp.get_indexes("ip_addresses")]
    except Exception:
        existing_ip_idx = []
    if "ix_ip_addresses_interface_id" not in existing_ip_idx:
        op.create_index("ix_ip_addresses_interface_id", "ip_addresses", ["interface_id"])

    # foreign key (best-effort)
    try:
        # see if FK exists by name; if not, create it
        # inspector doesn't list FK names easily across versions; just try/except creation
        op.create_foreign_key(
            "fk_ip_addresses_interface",
            "ip_addresses",
            "interfaces",
            ["interface_id"],
            ["id"],
            ondelete="SET NULL",
        )
    except Exception:
        pass


def downgrade() -> None:
    # drop FK & index on ip_addresses (best-effort)
    try:
        op.drop_constraint("fk_ip_addresses_interface", "ip_addresses", type_="foreignkey")
    except Exception:
        pass
    try:
        op.drop_index("ix_ip_addresses_interface_id", table_name="ip_addresses")
    except Exception:
        pass

    # drop cables (best-effort)
    try:
        op.drop_constraint("ck_cable_distinct_ends", "cables", type_="check")
    except Exception:
        pass
    try:
        op.drop_table("cables")
    except Exception:
        pass

    # drop interfaces (best-effort)
    try:
        op.drop_index("ix_interfaces_device_id", table_name="interfaces")
    except Exception:
        pass
    try:
        op.drop_constraint("uq_interfaces_device_name", "interfaces", type_="unique")
    except Exception:
        pass
    try:
        op.drop_table("interfaces")
    except Exception:
        pass
