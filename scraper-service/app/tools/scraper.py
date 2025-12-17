from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

from common_schemas import kafka_models


# TODO добавить парсинг sitemap
# TODO добавить проход по другим сущностям (по картинкам, стилям, и т.д.)
# TODO добавить проход по iframe и подобным ссылкам (нетипичным)
async def scraper_html(url_id: int, resp: aiohttp.ClientResponse) -> kafka_models.Res:
    html = await resp.text()
    soup = BeautifulSoup(html, "lxml")
    h1 = getattr(soup.find("h1"), "text", "").strip()
    title = getattr(soup.find("title"), "text", "").strip()
    description = (
        (tag := soup.find("meta", attrs={"name": "description"}))
        and tag.get("content", "").strip()
        or ""
    )
    canonical = (
        (tag := soup.find("link", attrs={"rel": "canonical"}))
        and tag.get("href", "").strip()
        or ""
    )
    # BEGIN follow
    global_follow = True
    if tag := soup.find("meta", attrs={"name": "robots"}):
        if "nofollow" in tag.get("content", "").lower():
            global_follow = False
    if tag := soup.find("meta", attrs={"name": "googlebot"}):
        if "nofollow" in tag.get("content", "").lower():
            global_follow = False
    # END follow ; BEGIN links
    links: list[kafka_models.Link] = []
    for tag in soup.find_all("a"):
        raw_url = tag.get("href", "")
        follow = False if "nofollow" in tag.get("rel", []) else global_follow
        if raw_url:
            links.append(
                kafka_models.Link(
                    tag="a",
                    attr="href",
                    field=raw_url.strip(),
                    full_url=urljoin(str(resp.url), raw_url.strip()),
                    follow=follow,
                )
            )
    # END links
    return kafka_models.Res(
        url_id=url_id,
        status_code=resp.status,
        content_type=resp.headers.get("content-type", ""),
        h1=h1,
        title=title,
        description=description,
        canonical=canonical,
        links=links,
    )


async def scraper_200(url_id: int, resp: aiohttp.ClientResponse) -> kafka_models.Res:
    if resp.headers.get("content-type", "").split(";")[0] == "text/html":
        return await scraper_html(url_id, resp)
    # else
    return kafka_models.Res(
        url_id=url_id,
        status_code=resp.status,
        content_type=resp.headers.get("content-type", ""),
    )
