from sqlalchemy import String, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, INET, CIDR
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from ..db import Base

class VRF(Base):
    __tablename__ = "vrfs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    rd: Mapped[str | None] = mapped_column(String(64))

class VLAN(Base):
    __tablename__ = "vlans"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    vid: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str | None] = mapped_column(String(128))
    __table_args__ = (
        UniqueConstraint("site_id", "vid", name="uq_vlan_site_vid"),
        CheckConstraint("vid >= 1 AND vid <= 4094", name="ck_vlan_vid_range"),
    )

class Prefix(Base):
    __tablename__ = "prefixes"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vrf_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("vrfs.id"))
    cidr: Mapped[str] = mapped_column(CIDR, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255))

class IPAddress(Base):
    __tablename__ = "ip_addresses"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vrf_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("vrfs.id"))
    address = mapped_column(INET, unique=True, index=True, nullable=False)
    # Remove FK for Phase 0.5; we’ll add proper Interfaces later
    interface_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    dns_name: Mapped[str | None] = mapped_column(String(255))
