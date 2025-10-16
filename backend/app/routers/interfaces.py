from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from ..utils.dbtools import session_scope
from ..models.core import Interface, Cable
from ..schemas import InterfaceIn, InterfaceOut, CableConnectIn, CableOut

router = APIRouter(prefix="/interfaces", tags=["interfaces"])

@router.get("", response_model=list[InterfaceOut])
def list_interfaces(device_id: str | None = Query(None)):
    with session_scope() as s:
        q = select(Interface)
        if device_id:
            q = q.where(Interface.device_id == device_id)
        rows = s.execute(q).scalars().all()
        return [InterfaceOut.model_validate(i) for i in rows]

@router.post("", response_model=InterfaceOut, status_code=201)
def create_interface(payload: InterfaceIn):
    with session_scope() as s:
        obj = Interface(**payload.dict())
        s.add(obj)
        try:
            s.flush()
        except IntegrityError:
            raise HTTPException(409, "Interface name already exists on this device.")
        return InterfaceOut.model_validate(obj)

@router.post("/connect", response_model=CableOut, status_code=201)
def connect(payload: CableConnectIn):
    if payload.a_interface_id == payload.b_interface_id:
        raise HTTPException(400, "Cannot connect an interface to itself.")
    with session_scope() as s:
        # ends must be free
        used = s.execute(
            select(Cable).where(
                or_(Cable.a_interface_id == payload.a_interface_id,
                    Cable.b_interface_id == payload.a_interface_id,
                    Cable.a_interface_id == payload.b_interface_id,
                    Cable.b_interface_id == payload.b_interface_id)
            )
        ).first()
        if used:
            raise HTTPException(409, "One or both interfaces already connected.")
        cab = Cable(**payload.dict())
        s.add(cab); s.flush()
        return CableOut.model_validate(cab)

@router.post("/disconnect/{interface_id}", status_code=204)
def disconnect(interface_id: str):
    with session_scope() as s:
        cab = s.execute(
            select(Cable).where(
                or_(Cable.a_interface_id == interface_id,
                    Cable.b_interface_id == interface_id)
            )
        ).scalars().first()
        if not cab:
            raise HTTPException(404, "Interface is not connected.")
        s.delete(cab); s.flush()
        return
