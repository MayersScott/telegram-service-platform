from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.db.session import get_session
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import AdminLogin

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(data: AdminLogin, session: AsyncSession = Depends(get_session)) -> Token:
    res = await session.execute(select(User).where(User.email == data.email))
    user = res.scalar_one_or_none()
    if user is None or not user.is_admin or not user.password_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials")

    token = create_access_token(subject=user.email or "")
    return Token(access_token=token)
