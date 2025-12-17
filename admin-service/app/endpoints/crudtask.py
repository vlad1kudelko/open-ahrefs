from urllib.parse import ParseResult, urlparse

from db.engine import session_factory
from fastapi import APIRouter
from tools.find_add_url import find_add_url

crudtask = APIRouter()


@crudtask.get("/addurl")
def api_addurl(url: str) -> str:
    parse_url: ParseResult = urlparse(url)
    if parse_url.scheme not in ["http", "https"]:
        return "ERROR scheme"
    if not parse_url.hostname:
        return "ERROR domain"
    with session_factory() as session:
        _, isNew = find_add_url(session, parse_url)
        if not isNew:
            return "ERROR idempotence"
        session.commit()
        return "OK"
