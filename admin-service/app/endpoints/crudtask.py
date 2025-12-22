from db.engine import async_session_factory
from db.models import Domain, Url
from fastapi import APIRouter
from sqlalchemy import select
from tools.url_to_obj import url_to_obj

crudtask = APIRouter()


@crudtask.get("/addurl")
async def api_addurl(url: str) -> str:
    obj_url: Url | None = url_to_obj(url)
    if obj_url is None:
        return "ERROR parse"
    async with async_session_factory() as session:
        session.add(Domain(domain=obj_url.hostname))
        stmt = select(Url).where(Url.url_hash == obj_url.url_hash)
        result = await session.execute(stmt)
        old_url: Url | None = result.scalar_one_or_none()
        if old_url:
            return "ERROR idempotence"
        else:
            session.add(obj_url)
            await session.commit()
            return "OK"
