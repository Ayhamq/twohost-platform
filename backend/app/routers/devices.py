from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from ..models.core import Device, Site
from ..schemas import DeviceIn, DeviceOut
from ..utils.dbtools import session_scope

router = APIRouter(prefix="/devices", tags=["devices"])

@router.patch("/{device_id}", response_model=DeviceOut)
def update_device(device_id: str, payload: dict):
    # payload may contain rack_id, position_u, and other optional fields
    allowed = {"vendor", "model", "role", "mgmt_ip", "rack_id", "position_u", "name"}
    updates = {k: v for k, v in payload.items() if k in allowed}

    with session_scope() as s:
        dev = s.get(Device, device_id)
        if not dev:
            raise HTTPException(404, "device not found")

        if "rack_id" in updates and updates["rack_id"] is not None:
            if not s.get(Rack, updates["rack_id"]):
                raise HTTPException(400, "rack_id not found")

        for k, v in updates.items():
            setattr(dev, k, v)

        try:
            s.flush()
        except IntegrityError:
            # e.g. name uniqueness per site
            raise HTTPException(409, "conflict updating device")

        return DeviceOut.model_validate(dev)

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
