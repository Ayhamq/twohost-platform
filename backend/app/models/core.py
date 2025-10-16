# ...existing imports...
from sqlalchemy import (
    String, ForeignKey, Integer, Boolean, UniqueConstraint, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, INET, MACADDR
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid
from ..utils.db import Base

class Site(Base):
    __tablename__ = "sites"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

    devices = relationship("Device", back_populates="site", cascade="all, delete-orphan")
    racks = relationship("Rack", back_populates="site", cascade="all, delete-orphan")  # NEW


class Rack(Base):
    __tablename__ = "racks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    u_height: Mapped[int] = mapped_column(Integer, nullable=False, default=42)  # 42U by default

    __table_args__ = (
        UniqueConstraint("site_id", "name", name="uq_racks_site_name"),
    )

    site = relationship("Site", back_populates="racks")
    devices = relationship("Device", back_populates="rack")  # optional backref for convenience


class Device(Base):
    __tablename__ = "devices"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    vendor: Mapped[str | None] = mapped_column(String(64))
    model: Mapped[str | None] = mapped_column(String(64))
    role: Mapped[str | None] = mapped_column(String(64))
    mgmt_ip = mapped_column(INET, nullable=True)

    # NEW (optional): place a device in a rack + position
    rack_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("racks.id", ondelete="SET NULL"), nullable=True, index=True)
    position_u: Mapped[int | None] = mapped_column(Integer, nullable=True)

    site = relationship("Site", back_populates="devices")
    rack = relationship("Rack", back_populates="devices")

class Interface(Base):
    __tablename__ = "interfaces"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)   # e.g. Gi1/0/1
    type: Mapped[str] = mapped_column(String(32), nullable=False, default="ethernet")
    admin_up: Mapped[bool] = mapped_column(Boolean, default=True)
    oper_up: Mapped[bool] = mapped_column(Boolean, default=False)
    mtu: Mapped[int | None] = mapped_column(Integer)
    mac = mapped_column(MACADDR, nullable=True)
    description: Mapped[str | None] = mapped_column(String(255))

    __table_args__ = (UniqueConstraint("device_id", "name", name="uq_interfaces_device_name"),)

    device = relationship("Device", backref="interfaces")

class Cable(Base):
    __tablename__ = "cables"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    a_interface_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("interfaces.id", ondelete="CASCADE"), unique=True, nullable=False)
    b_interface_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("interfaces.id", ondelete="CASCADE"), unique=True, nullable=False)
    label: Mapped[str | None] = mapped_column(String(64))
    color: Mapped[str | None] = mapped_column(String(16))

    __table_args__ = (CheckConstraint("a_interface_id <> b_interface_id", name="ck_cable_distinct_ends"),)

    a_interface = relationship("Interface", foreign_keys=[a_interface_id])
    b_interface = relationship("Interface", foreign_keys=[b_interface_id])
