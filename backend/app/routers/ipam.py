from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from uuid import UUID
from ..utils.dbtools import session_scope
from ..models.ipam import VRF, VLAN, Prefix, IPAddress
from ..models.core import Site
from ..schemas import VRFIn, VRFOut, VLANIn, VLANOut, PrefixIn, PrefixOut, IPAddressIn, IPAddressOut

router = APIRouter(prefix="/ipam", tags=["ipam"])

@router.post("/vrfs", response_model=VRFOut, status_code=201)
def create_vrf(payload: VRFIn):
    with session_scope() as s:
        if s.execute(select(VRF).where(VRF.name == payload.name)).scalar_one_or_none():
            raise HTTPException(409, "VRF exists")
        vrf = VRF(name=payload.name, rd=payload.rd)
        s.add(vrf); s.flush()
        return VRFOut(id=vrf.id, **payload.dict())

@router.get("/vrfs", response_model=list[VRFOut])
def list_vrfs():
    with session_scope() as s:
        return [VRFOut(id=x.id, name=x.name, rd=x.rd) for x in s.execute(select(VRF)).scalars()]

@router.post("/vlans", response_model=VLANOut, status_code=201)
def create_vlan(payload: VLANIn):
    with session_scope() as s:
        if not s.get(Site, payload.site_id):
            raise HTTPException(400, "site_id not found")
        vlan = VLAN(site_id=payload.site_id, vid=payload.vid, name=payload.name)
        s.add(vlan); s.flush()
        return VLANOut(id=vlan.id, **payload.dict())

@router.get("/vlans", response_model=list[VLANOut])
def list_vlans(site_id: UUID | None = None):
    with session_scope() as s:
        stmt = select(VLAN)
        if site_id: stmt = stmt.where(VLAN.site_id == site_id)
        return [VLANOut(id=x.id, site_id=x.site_id, vid=x.vid, name=x.name) for x in s.execute(stmt).scalars()]

@router.post("/prefixes", response_model=PrefixOut, status_code=201)
def create_prefix(payload: PrefixIn):
    with session_scope() as s:
        p = Prefix(vrf_id=payload.vrf_id, cidr=str(payload.cidr), description=payload.description)
        s.add(p); s.flush()
        return PrefixOut(id=p.id, vrf_id=p.vrf_id, cidr=payload.cidr, description=payload.description)

@router.get("/prefixes", response_model=list[PrefixOut])
def list_prefixes():
    with session_scope() as s:
        return [PrefixOut(id=x.id, vrf_id=x.vrf_id, cidr=x.cidr, description=x.description) for x in s.execute(select(Prefix)).scalars()]

@router.post("/ip-addresses", response_model=IPAddressOut, status_code=201)
def create_ip(payload: IPAddressIn):
    with session_scope() as s:
        ip = IPAddress(vrf_id=payload.vrf_id, address=str(payload.address), interface_id=payload.interface_id, dns_name=payload.dns_name)
        s.add(ip); s.flush()
        return IPAddressOut(id=ip.id, vrf_id=ip.vrf_id, address=payload.address, interface_id=ip.interface_id, dns_name=ip.dns_name)

@router.get("/ip-addresses", response_model=list[IPAddressOut])
def list_ips():
    with session_scope() as s:
        return [IPAddressOut(id=x.id, vrf_id=x.vrf_id, address=x.address, interface_id=x.interface_id, dns_name=x.dns_name) for x in s.execute(select(IPAddress)).scalars()]
