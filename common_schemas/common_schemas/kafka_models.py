from pydantic import BaseModel


class Url(BaseModel):
    url_id: int
    url: str


class Link(BaseModel):
    tag: str
    attr: str | None
    field: str


class Res(BaseModel):
    url_id: int
    status_code: int
    h1: str | None
    title: str | None
    description: str | None
    canonical: str | None
    redirect: str | None
    links: list[Link]
