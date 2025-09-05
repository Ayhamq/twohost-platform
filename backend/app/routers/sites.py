from fastapi import APIRouter
from sqlalchemy import select
from ..schemas import SiteIn, SiteOut
from ..models.core import Site
from ..utils.dbtools import session_scope

router = APIRouter(prefix="/sites", tags=["sites"])

@router.post("", response_model=SiteOut, status_code=201)
def create_site(payload: SiteIn):
    with session_scope() as s:
        site = Site(name=payload.name, slug=payload.slug)
        s.add(site); s.flush()
        return SiteOut(id=site.id, **payload.dict())

@router.get("", response_model=list[SiteOut])
def list_sites():
    with session_scope() as s:
        return [SiteOut(id=x.id, name=x.name, slug=x.slug) for x in s.execute(select(Site)).scalars()]
