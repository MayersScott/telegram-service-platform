from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class RequestCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=10_000)
    tg_user_id: int | None = None
    tg_chat_id: int | None = None


class RequestUpdateStatus(BaseModel):
    status: str = Field(min_length=1, max_length=32)


class RequestOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    tg_user_id: int | None
    tg_chat_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
