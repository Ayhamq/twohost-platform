from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from ..models.core import Device, Site
from ..schemas import DeviceIn, DeviceOut
from ..utils.dbtools import session_scope

router = APIRouter(prefix="/devices", tags=["devices"])

@router.get("", response_model=list[DeviceOut])
def list_devices():
    with session_scope() as s:
        rows = s.execute(select(Device)).scalars().all()
        return [DeviceOut.model_validate(obj) for obj in rows]  # materialize now

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
            role=payload.role,
            mgmt_ip=payload.mgmt_ip,
        )
        s.add(dev)
        try:
            s.flush()
        except IntegrityError:
            raise HTTPException(409, "A device with this name already exists in this site.")
        return DeviceOut.model_validate(dev)  # materialize now
