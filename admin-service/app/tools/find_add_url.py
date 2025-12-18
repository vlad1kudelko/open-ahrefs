import hashlib
from urllib.parse import ParseResult

from db.models import Url
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def find_add_url(
    session: AsyncSession, parse_url: ParseResult
) -> tuple[Url, bool]:
    """
    возвращаем кортеж с объектом и признаком того,
    новый это элемент (True) или найденный (False)
    """
    item_url: Url = Url(
        scheme=parse_url.scheme,
        domain=parse_url.hostname,
    )
    item_url.port = parse_url.port or item_url.port
    item_url.path = parse_url.path or item_url.path
    item_url.param = parse_url.query or item_url.param
    item_url.anchor = parse_url.fragment or item_url.anchor
    full_str: str = " ".join(
        [
            item_url.scheme,
            item_url.domain,
            str(item_url.port),
            str(item_url.path),
            str(item_url.param),
            str(item_url.anchor),
        ]
    )
    item_url.url_hash = hashlib.sha256(full_str.encode("utf-8")).hexdigest()
    stmt = select(Url).where(Url.url_hash == item_url.url_hash)
    result = await session.execute(stmt)
    old_url: Url | None = result.scalar_one_or_none()
    if old_url:
        return (old_url, False)
    else:
        session.add(item_url)
        await session.flush()
        return (item_url, True)
