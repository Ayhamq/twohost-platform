from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from ..schemas import DeviceIn, DeviceOut
from ..models.core import Device, Site
from ..utils.dbtools import session_scope

router = APIRouter(prefix="/devices", tags=["devices"])

@router.post("", response_model=DeviceOut, status_code=201)
def create_device(payload: DeviceIn):
    with session_scope() as s:
        if not s.get(Site, payload.site_id):
            raise HTTPException(400, "site_id not found")
        dev = Device(
            site_id=payload.site_id,
            name=payload.name,
            vendor=payload.vendor,
            model=payload.model,
            role=payload.role,  # pass through
            mgmt_ip=str(payload.mgmt_ip) if payload.mgmt_ip else None,
        )
        s.add(dev); s.flush()
        return DeviceOut(id=dev.id, **payload.dict())

@router.get("", response_model=list[DeviceOut])
def list_devices():
    with session_scope() as s:
        rows = s.execute(select(Device)).scalars().all()
        return [
            DeviceOut(
                id=d.id,
                site_id=d.site_id,
                name=d.name,
                vendor=d.vendor,
                model=d.model,
                role=d.role,
                mgmt_ip=str(d.mgmt_ip) if d.mgmt_ip else None,  # ← cast INET to str
            )
            for d in rows
        ]
