from sqlalchemy import select, BigInteger

from database.models import async_session, User


async def set_user(tg_id: int, filter_href: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, filter_href=filter_href))
            await session.commit()
