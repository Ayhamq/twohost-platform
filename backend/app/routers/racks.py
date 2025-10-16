from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from ..utils.dbtools import session_scope
from ..models.core import Rack, Site
from ..schemas import RackIn, RackOut

router = APIRouter(prefix="/racks", tags=["racks"])

@router.get("", response_model=list[RackOut])
def list_racks():
    with session_scope() as s:
        rows = s.execute(select(Rack)).scalars().all()
        return [RackOut.model_validate(r) for r in rows]

@router.post("", response_model=RackOut, status_code=201)
def create_rack(payload: RackIn):
    with session_scope() as s:
        if not s.get(Site, payload.site_id):
            raise HTTPException(400, "site_id not found")
        rack = Rack(site_id=payload.site_id, name=payload.name, u_height=payload.u_height)
        s.add(rack)
        try:
            s.flush()
        except IntegrityError:
            raise HTTPException(409, "A rack with this name already exists in this site.")
        return RackOut.model_validate(rack)

@router.get("/{rack_id}", response_model=RackOut)
def get_rack(rack_id: str):
    with session_scope() as s:
        r = s.get(Rack, rack_id)
        if not r:
            raise HTTPException(404, "rack not found")
        return RackOut.model_validate(r)

@router.delete("/{rack_id}", status_code=204)
def delete_rack(rack_id: str):
    with session_scope() as s:
        r = s.get(Rack, rack_id)
        if not r:
            raise HTTPException(404, "rack not found")
        s.delete(r)
        s.flush()
        return
