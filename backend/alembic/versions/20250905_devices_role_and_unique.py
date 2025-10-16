"""add role column and make device name unique per site"""

from alembic import op
import sqlalchemy as sa

revision = "20250905_devices_role_and_unique"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)

    # add 'role' if missing
    cols = [c["name"] for c in insp.get_columns("devices")]
    if "role" not in cols:
        op.add_column("devices", sa.Column("role", sa.String(length=64), nullable=True))

    # drop unique(name) if exists
    try:
        op.drop_constraint("devices_name_key", "devices", type_="unique")
    except Exception:
        pass

    # create unique(site_id, name) if not exists (best-effort)
    try:
        op.create_unique_constraint("uq_devices_site_name", "devices", ["site_id", "name"])
    except Exception:
        pass

def downgrade() -> None:
    # revert unique(site_id, name)
    try:
        op.drop_constraint("uq_devices_site_name", "devices", type_="unique")
    except Exception:
        pass

    # restore unique(name)
    try:
        op.create_unique_constraint("devices_name_key", "devices", ["name"])
    except Exception:
        pass

    # drop 'role' if present
    bind = op.get_bind()
    insp = sa.inspect(bind)
    cols = [c["name"] for c in insp.get_columns("devices")]
    if "role" in cols:
        op.drop_column("devices", "role")
