from decimal import Decimal
from typing import Any

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, MappedColumn, relationship

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: MappedColumn[Any] = mapped_column(BigInteger)
    filter_href: Mapped[str] = mapped_column(String(500))


class AvitoEntity(Base):
    __tablename__ = 'avito_entities'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    price: Mapped[Decimal] = mapped_column()
    href: Mapped[str] = mapped_column(String(500))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
