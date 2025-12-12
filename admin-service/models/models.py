from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated
import datetime
import sqlalchemy as sa

created_at = Annotated[datetime.datetime, mapped_column(sa.DateTime, server_default=sa.text("TIMEZONE('utc', now())"))]

class Base(DeclarativeBase):
    pass


class Url(Base):
    __tablename__ = 'urls'
    url_id     : Mapped[int]        = mapped_column(sa.BigInteger, primary_key=True)
    created_at : Mapped[created_at]
    scheme     : Mapped[str]        = mapped_column(sa.String(16))
    domain     : Mapped[str]        = mapped_column(sa.String(256))
    port       : Mapped[int | None] = mapped_column(sa.Integer, sa.CheckConstraint('port > 0'))
    path       : Mapped[str | None] = mapped_column(sa.Text)
    param      : Mapped[str | None] = mapped_column(sa.Text)
    anchor     : Mapped[str | None] = mapped_column(sa.Text)


class Response(Base):
    __tablename__ = 'responses'
    response_id : Mapped[int]        = mapped_column(sa.BigInteger, primary_key=True)
    created_at  : Mapped[created_at]
    url_id      : Mapped[int]        = mapped_column(sa.BigInteger, sa.ForeignKey('urls.url_id'))
    status_code : Mapped[int]        = mapped_column(sa.Integer, sa.CheckConstraint('status_code >= 100 AND status_code < 600'))
    h1          : Mapped[str | None] = mapped_column(sa.Text)
    title       : Mapped[str | None] = mapped_column(sa.Text)
    description : Mapped[str | None] = mapped_column(sa.Text)
    canonical   : Mapped[str | None] = mapped_column(sa.Text)
    redirect    : Mapped[str | None] = mapped_column(sa.Text)


class Link(Base):
    __tablename__ = 'links'
    link_id       : Mapped[int]        = mapped_column(sa.BigInteger, primary_key=True)
    created_at    : Mapped[created_at]
    source_url_id : Mapped[int]        = mapped_column(sa.BigInteger, sa.ForeignKey('urls.url_id'))
    target_url_id : Mapped[int]        = mapped_column(sa.BigInteger, sa.ForeignKey('urls.url_id'))
    tag           : Mapped[str]        = mapped_column(sa.String(16))
    attr          : Mapped[str | None] = mapped_column(sa.String(16))
    field         : Mapped[str]        = mapped_column(sa.Text)
