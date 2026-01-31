from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def upsert_telegram_user(session: AsyncSession, tg_user_id: int, tg_chat_id: int) -> User:
    res = await session.execute(select(User).where(User.tg_user_id == tg_user_id))
    user = res.scalar_one_or_none()
    if user is None:
        user = User(tg_user_id=tg_user_id, tg_chat_id=tg_chat_id, is_admin=False)
        session.add(user)
    else:
        user.tg_chat_id = tg_chat_id
    await session.commit()
    await session.refresh(user)
    return user
