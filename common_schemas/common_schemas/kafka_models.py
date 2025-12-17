from pydantic import BaseModel


class Url(BaseModel):
    url_id: int
    url: str


class Link(BaseModel):
    tag: str
    attr: str | None = None
    field: str
    full_url: str
    follow: bool = True


class Res(BaseModel):
    url_id: int
    status_code: int
    content_type: str
    h1: str | None = None
    title: str | None = None
    description: str | None = None
    canonical: str | None = None
    redirect: str | None = None
    links: list[Link] | None = None
