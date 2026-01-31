from __future__ import annotations

from fastapi import APIRouter

from app.api.routes import auth, requests, telegram

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(telegram.router, prefix="/public/telegram", tags=["telegram"])
api_router.include_router(requests.router, prefix="/requests", tags=["requests"])
