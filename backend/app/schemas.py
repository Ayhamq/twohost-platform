from pydantic import BaseModel, IPvAnyAddress, IPvAnyNetwork, constr, field_validator
from uuid import UUID

class SiteIn(BaseModel):
    name: constr(strip_whitespace=True, min_length=2)
    slug: constr(pattern=r"^[a-z0-9\-]+$")
class SiteOut(SiteIn):
    id: UUID

class DeviceIn(BaseModel):
    site_id: UUID
    name: constr(strip_whitespace=True, min_length=2)
    vendor: str | None = None
    model: str | None = None
    role: str | None = None  # NEW
    mgmt_ip: IPvAnyAddress | None = None
class DeviceOut(DeviceIn):
    id: UUID

class VRFIn(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    rd: str | None = None
class VRFOut(VRFIn):
    id: UUID

class VLANIn(BaseModel):
    site_id: UUID
    vid: int
    name: str | None = None
    @field_validator("vid")
    @classmethod
    def check_vid(cls, v): 
        if not 1 <= v <= 4094: raise ValueError("VLAN must be 1..4094")
        return v
class VLANOut(VLANIn):
    id: UUID

class PrefixIn(BaseModel):
    vrf_id: UUID | None = None
    cidr: IPvAnyNetwork
    description: str | None = None
class PrefixOut(PrefixIn):
    id: UUID

class IPAddressIn(BaseModel):
    vrf_id: UUID | None = None
    address: IPvAnyAddress
    interface_id: UUID | None = None
    dns_name: str | None = None
class IPAddressOut(IPAddressIn):
    id: UUID
