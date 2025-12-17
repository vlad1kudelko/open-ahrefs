from urllib.parse import ParseResult

from db.models import Url
from sqlalchemy.orm import Session


def find_add_url(session: Session, parse_url: ParseResult) -> tuple[Url, bool]:
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
    old_url: Url = (
        session.query(Url)
        .filter(Url.scheme == item_url.scheme)
        .filter(Url.domain == item_url.domain)
        .filter(Url.port == item_url.port)
        .filter(Url.path == item_url.path)
        .filter(Url.param == item_url.param)
        .filter(Url.anchor == item_url.anchor)
        .one_or_none()
    )
    if old_url:
        return (old_url, False)
    else:
        session.add(item_url)
        session.flush()
        return (item_url, True)
