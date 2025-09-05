from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

class SiteIn(BaseModel):
    name: str
    slug: str

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

class DeviceOut(BaseModel):
    id: UUID
    site_id: UUID
    name: str
    vendor: Optional[str] = None
    model: Optional[str] = None
    role: Optional[str] = None
    mgmt_ip: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)  # important for ORM objects
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
