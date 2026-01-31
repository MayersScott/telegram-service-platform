from __future__ import annotations

from pydantic import BaseModel, EmailStr


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class TelegramUpsert(BaseModel):
    tg_user_id: int
    tg_chat_id: int


class UserOut(BaseModel):
    id: int
    email: EmailStr | None
    is_admin: bool
    tg_user_id: int | None
    tg_chat_id: int | None

    model_config = {"from_attributes": True}
