from __future__ import annotations

import logging

from sqlalchemy import select

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.user import User

logger = logging.getLogger(__name__)


async def ensure_admin_user() -> None:
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User).where(User.email == settings.admin_email))
        user = res.scalar_one_or_none()
        if user:
            return

        user = User(
            email=settings.admin_email,
            password_hash=hash_password(settings.admin_password),
            is_admin=True,
        )
        session.add(user)
        await session.commit()
        logger.info("Admin user created: %s", settings.admin_email)
