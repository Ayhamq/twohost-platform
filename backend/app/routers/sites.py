from fastapi import APIRouter
from sqlalchemy import select
from ..models.core import Site
from ..schemas import SiteIn, SiteOut
from ..utils.dbtools import session_scope

router = APIRouter(prefix="/sites", tags=["sites"])

@router.get("", response_model=list[SiteOut])
def list_sites():
    with session_scope() as s:
        rows = s.execute(select(Site)).scalars().all()
        # Convert to Pydantic objects while session is open
        return [SiteOut.model_validate(obj) for obj in rows]

@router.post("", response_model=SiteOut, status_code=201)
def create_site(payload: SiteIn):
    with session_scope() as s:
        site = Site(name=payload.name, slug=payload.slug)
        s.add(site)
        s.flush()
        return SiteOut.model_validate(site)
