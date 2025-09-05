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

    # 1) add 'role' column if it doesn't exist
    cols = {c['name'] for c in insp.get_columns('devices')}
    if 'role' not in cols:
        op.add_column('devices', sa.Column('role', sa.String(length=64), nullable=True))

    # 2) ensure unique(site_id, name)
    uqs = {uc['name']: uc for uc in insp.get_unique_constraints('devices')}
    if 'devices_name_key' in uqs:
        op.drop_constraint('devices_name_key', 'devices', type_='unique')
    if 'uq_devices_site_name' not in uqs:
        op.create_unique_constraint('uq_devices_site_name', 'devices', ['site_id', 'name'])

def downgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)

    uqs = {uc['name']: uc for uc in insp.get_unique_constraints('devices')}
    if 'uq_devices_site_name' in uqs:
        op.drop_constraint('uq_devices_site_name', 'devices', type_='unique')
    if 'devices_name_key' not in uqs:
        op.create_unique_constraint('devices_name_key', 'devices', ['name'])

    cols = {c['name'] for c in insp.get_columns('devices')}
    if 'role' in cols:
        op.drop_column('devices', 'role')
