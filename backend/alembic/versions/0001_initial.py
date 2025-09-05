"""initial schema for 2-Host Phase 0.5

Revision ID: 0001_initial
Revises: 
Create Date: 2025-09-05
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('sites',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False, unique=True),
        sa.Column('slug', sa.String(length=128), nullable=False, unique=True),
    )

    op.create_table('vrfs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False, unique=True),
        sa.Column('rd', sa.String(length=64), nullable=True),
    )

    op.create_table('devices',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('site_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('sites.id'), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False, unique=True),
        sa.Column('vendor', sa.String(length=64), nullable=True),
        sa.Column('model', sa.String(length=64), nullable=True),
        sa.Column('mgmt_ip', postgresql.INET, nullable=True),
    )
    op.create_index('ix_devices_site_id', 'devices', ['site_id'])

    op.create_table('vlans',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('site_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('sites.id', ondelete='CASCADE'), nullable=False),
        sa.Column('vid', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=True),
    )
    op.create_index('ix_vlans_site_id', 'vlans', ['site_id'])
    op.create_unique_constraint('uq_vlan_site_vid', 'vlans', ['site_id', 'vid'])

    op.create_table('prefixes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('vrf_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('vrfs.id'), nullable=True),
        sa.Column('cidr', postgresql.CIDR, nullable=False, unique=True),
        sa.Column('description', sa.String(length=255), nullable=True),
    )
    op.create_index('ix_prefixes_vrf_id', 'prefixes', ['vrf_id'])

    op.create_table('ip_addresses',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('vrf_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('vrfs.id'), nullable=True),
        sa.Column('address', postgresql.INET, nullable=False, unique=True),
        sa.Column('interface_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('dns_name', sa.String(length=255), nullable=True),
    )
    op.create_index('ix_ip_addresses_vrf_id', 'ip_addresses', ['vrf_id'])


def downgrade() -> None:
    op.drop_index('ix_ip_addresses_vrf_id', table_name='ip_addresses')
    op.drop_table('ip_addresses')
    op.drop_index('ix_prefixes_vrf_id', table_name='prefixes')
    op.drop_table('prefixes')
    op.drop_constraint('uq_vlan_site_vid', 'vlans', type_='unique')
    op.drop_index('ix_vlans_site_id', table_name='vlans')
    op.drop_table('vlans')
    op.drop_index('ix_devices_site_id', table_name='devices')
    op.drop_table('devices')
    op.drop_table('vrfs')
    op.drop_table('sites')
