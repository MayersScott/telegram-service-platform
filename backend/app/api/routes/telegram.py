from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.user import TelegramUpsert, UserOut
from app.services.users import upsert_telegram_user

router = APIRouter()


@router.post("/upsert", response_model=UserOut)
async def telegram_upsert(data: TelegramUpsert, session: AsyncSession = Depends(get_session)) -> UserOut:
    user = await upsert_telegram_user(session, tg_user_id=data.tg_user_id, tg_chat_id=data.tg_chat_id)
    return UserOut.model_validate(user)
