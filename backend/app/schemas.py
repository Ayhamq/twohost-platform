from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

class SiteIn(BaseModel):
    name: str
    slug: str

class RackIn(BaseModel):
    site_id: UUID
    name: str
    u_height: int = 42

class RackOut(BaseModel):
    id: UUID
    site_id: UUID
    name: str
    u_height: int
    model_config = ConfigDict(from_attributes=True)

class SiteOut(BaseModel):
    id: UUID
    name: str
    slug: str
    model_config = ConfigDict(from_attributes=True)  # important for ORM objects

class DeviceIn(BaseModel):
    site_id: UUID
    name: str
    vendor: Optional[str] = None
    model: Optional[str] = None
    role: Optional[str] = None
    mgmt_ip: Optional[str] = None
    rack_id: Optional[UUID] = None       # NEW (optional)
    position_u: Optional[int] = None     # NEW (optional)

class DeviceOut(BaseModel):
    id: UUID
    site_id: UUID
    name: str
    vendor: Optional[str] = None
    model: Optional[str] = None
    role: Optional[str] = None
    mgmt_ip: Optional[str] = None
    rack_id: Optional[UUID] = None       # NEW (optional)
    position_u: Optional[int] = None     # NEW (optional)
    model_config = ConfigDict(from_attributes=True)
# ---------- VRF ----------
class VRFIn(BaseModel):
    name: str
    rd: Optional[str] = None

class VRFOut(BaseModel):
    id: UUID
    name: str
    rd: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# ---------- VLAN ----------
class VLANIn(BaseModel):
    site_id: UUID
    vid: int
    name: Optional[str] = None

class VLANOut(BaseModel):
    id: UUID
    site_id: UUID
    vid: int
    name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# ---------- Prefix ----------
class PrefixIn(BaseModel):
    vrf_id: Optional[UUID] = None
    cidr: str
    description: Optional[str] = None

class PrefixOut(BaseModel):
    id: UUID
    vrf_id: Optional[UUID] = None
    cidr: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# ---------- IP Address ----------
class IPAddressIn(BaseModel):
    vrf_id: Optional[UUID] = None
    address: str
    interface_id: Optional[UUID] = None
    dns_name: Optional[str] = None

class IPAddressOut(BaseModel):
    id: UUID
    vrf_id: Optional[UUID] = None
    address: str
    interface_id: Optional[UUID] = None
    dns_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class InterfaceIn(BaseModel):
    device_id: UUID
    name: str
    type: str = "ethernet"
    admin_up: bool = True
    mtu: Optional[int] = None
    mac: Optional[str] = None
    description: Optional[str] = None

class InterfaceOut(BaseModel):
    id: UUID
    device_id: UUID
    name: str
    type: str
    admin_up: bool
    oper_up: bool
    mtu: Optional[int]
    mac: Optional[str]
    description: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class CableConnectIn(BaseModel):
    a_interface_id: UUID
    b_interface_id: UUID
    label: Optional[str] = None
    color: Optional[str] = None

class CableOut(BaseModel):
    id: UUID
    a_interface_id: UUID
    b_interface_id: UUID
    label: Optional[str]
    color: Optional[str]
    model_config = ConfigDict(from_attributes=True)
