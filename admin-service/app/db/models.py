from datetime import datetime
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

created_at = Annotated[
    datetime,
    mapped_column(sa.DateTime, server_default=sa.text("TIMEZONE('utc', now())")),
]


class Base(DeclarativeBase):
    pass


class Url(Base):
    __tablename__ = "urls"
    __table_args__ = (sa.CheckConstraint("port >= 0 AND port <= 65535"),)
    url_id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    created_at: Mapped[created_at]
    scheme: Mapped[str] = mapped_column(sa.String(16))
    domain: Mapped[str] = mapped_column(sa.String(256))
    port: Mapped[int | None] = mapped_column(sa.Integer)
    path: Mapped[str | None] = mapped_column(sa.Text)
    param: Mapped[str | None] = mapped_column(sa.Text)
    anchor: Mapped[str | None] = mapped_column(sa.Text)
    last_pars: Mapped[datetime | None] = mapped_column(sa.DateTime)


class Response(Base):
    __tablename__ = "responses"
    __table_args__ = (sa.CheckConstraint("status_code >= 100 AND status_code < 600"),)
    response_id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    created_at: Mapped[created_at]
    url_id: Mapped[int] = mapped_column(sa.BigInteger, sa.ForeignKey("urls.url_id"))
    status_code: Mapped[int] = mapped_column(sa.Integer)
    content_type: Mapped[str] = mapped_column(sa.String(256))
    h1: Mapped[str | None] = mapped_column(sa.Text)
    title: Mapped[str | None] = mapped_column(sa.Text)
    description: Mapped[str | None] = mapped_column(sa.Text)
    canonical: Mapped[str | None] = mapped_column(sa.Text)
    redirect: Mapped[str | None] = mapped_column(sa.Text)


class Link(Base):
    __tablename__ = "links"
    link_id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    created_at: Mapped[created_at]
    source_url_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey("urls.url_id")
    )
    target_url_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey("urls.url_id")
    )
    tag: Mapped[str] = mapped_column(sa.String(16))
    attr: Mapped[str | None] = mapped_column(sa.String(16))
    field: Mapped[str] = mapped_column(sa.Text)
    follow: Mapped[bool] = mapped_column(sa.Boolean)
