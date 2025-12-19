import hashlib
from urllib.parse import ParseResult, urlparse

from db.models import Url


def url_to_obj(url: str) -> Url | None:
    """
    функция преобразования строки со ссылкой в объект модели
    """
    parse_url: ParseResult = urlparse(url, scheme="https")
    if parse_url.scheme not in ["http", "https"]:
        return None
    if not parse_url.hostname:
        return None
    obj_url: Url = Url(
        url_hash=hashlib.sha256(parse_url.geturl().encode("utf-8")).hexdigest(),
        scheme=parse_url.scheme,
        username=parse_url.username or None,
        password=parse_url.password or None,
        hostname=parse_url.hostname,
        port=parse_url.port or None,
        path=parse_url.path or None,
        params=parse_url.params or None,
        query=parse_url.query or None,
        fragment=parse_url.fragment or None,
        full_url=parse_url.geturl(),
    )
    return obj_url


def obj_to_dict(list_urls: list[Url]) -> list[dict]:
    return [
        {
            "url_hash": u.url_hash,
            "scheme": u.scheme,
            "username": u.username,
            "password": u.password,
            "hostname": u.hostname,
            "port": u.port,
            "path": u.path,
            "params": u.params,
            "query": u.query,
            "fragment": u.fragment,
            "full_url": u.full_url,
        }
        for u in list_urls
    ]
