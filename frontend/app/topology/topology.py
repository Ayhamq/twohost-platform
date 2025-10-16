from fastapi import APIRouter
from sqlalchemy import select
from ..utils.dbtools import session_scope
from ..models.core import Device, Interface, Cable

router = APIRouter(prefix="/topology", tags=["topology"])

@router.get("")
def topology():
    with session_scope() as s:
        devs = s.execute(select(Device)).scalars().all()
        ifs  = s.execute(select(Interface)).scalars().all()
        cabs = s.execute(select(Cable)).scalars().all()

        nodes = [{"id": str(d.id), "label": d.name, "group": d.role or "device"} for d in devs]
        # map interface -> device
        dev_by_if = {str(i.id): str(i.device_id) for i in ifs}
        edges = []
        for c in cabs:
            a = dev_by_if.get(str(c.a_interface_id))
            b = dev_by_if.get(str(c.b_interface_id))
            if a and b and a != b:
                edges.append({"from": a, "to": b})
        return {"nodes": nodes, "edges": edges}
