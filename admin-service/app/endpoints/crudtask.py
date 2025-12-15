from urllib.parse import urlparse

from app.db.engine import session_factory
from app.db.models import Url
from fastapi import APIRouter

crudtask = APIRouter()


@crudtask.get("/addurl")
def api_addurl(domain: str) -> str:
    if not urlparse(domain).scheme:
        return "ERROR scheme"
    if not urlparse(domain).netloc:
        return "ERROR domain"
    with session_factory() as session:
        item_url = Url(
            scheme=urlparse(domain).scheme,
            domain=urlparse(domain).netloc.split(":")[0],
        )
        if len(urlparse(domain).netloc.split(":")) == 2:
            item_url.port = int(urlparse(domain).netloc.split(":")[1])
        if urlparse(domain).path:
            item_url.path = urlparse(domain).path
        if urlparse(domain).query:
            item_url.param = urlparse(domain).query
        if urlparse(domain).fragment:
            item_url.anchor = urlparse(domain).fragment
        session.add(item_url)
        # add kafka
        session.commit()
        return "OK"
