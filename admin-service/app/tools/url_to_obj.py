import hashlib
from urllib.parse import ParseResult, urlparse

from db.models import Url


def url_to_obj(url: str) -> Url | None:
    """
    функция преобразования строки со ссылкой в объект модели
    """
    parse_url: ParseResult = urlparse(url)
    if parse_url.scheme not in ["http", "https"]:
        return None
    if not parse_url.hostname:
        return None

    obj_url: Url = Url(
        scheme=parse_url.scheme,
        domain=parse_url.hostname,
    )
    obj_url.port = parse_url.port or None
    obj_url.path = parse_url.path or None
    obj_url.param = parse_url.query or None
    obj_url.anchor = parse_url.fragment or None
    full_str: str = " ".join(
        [
            obj_url.scheme,
            obj_url.domain,
            str(obj_url.port),
            str(obj_url.path),
            str(obj_url.param),
            str(obj_url.anchor),
        ]
    )
    obj_url.url_hash = hashlib.sha256(full_str.encode("utf-8")).hexdigest()
    return obj_url


def obj_to_list_dict(list_urls: list[Url]) -> list[dict]:
    return [
        {
            "url_hash": u.url_hash,
            "scheme": u.scheme,
            "domain": u.domain,
            "port": u.port,
            "path": u.path,
            "param": u.param,
            "anchor": u.anchor,
        }
        for u in list_urls
    ]
