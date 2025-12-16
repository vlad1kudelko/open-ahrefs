from urllib.parse import ParseResult, urlparse

from db.engine import session_factory
from db.models import Url
from fastapi import APIRouter

crudtask = APIRouter()


@crudtask.get("/addurl")
def api_addurl(url: str) -> str:
    parse_url: ParseResult = urlparse(url)
    if not parse_url.scheme:
        return "ERROR scheme"
    if not parse_url.netloc:
        return "ERROR domain"
    host: str = parse_url.netloc
    port: str | None = None
    if ":" in parse_url.netloc:
        host, port = parse_url.netloc.split(":")
    item_url = Url(scheme=parse_url.scheme, domain=host)
    item_url.port = int(port) if port else None
    item_url.path = parse_url.path or item_url.path
    item_url.param = parse_url.query or item_url.param
    item_url.anchor = parse_url.fragment or item_url.anchor
    with session_factory() as session:
        count: int = (
            session.query(Url)
            .filter(Url.scheme == item_url.scheme)
            .filter(Url.domain == item_url.domain)
            .filter(Url.port == item_url.port)
            .filter(Url.path == item_url.path)
            .filter(Url.param == item_url.param)
            .filter(Url.anchor == item_url.anchor)
            .count()
        )
        if count > 0:
            return "ERROR idempotence"
        session.add(item_url)
        session.commit()
        return "OK"
