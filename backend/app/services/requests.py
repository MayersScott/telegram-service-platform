from __future__ import annotations

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request import Request
from app.schemas.request import RequestCreate
from app.tasks.notifications import notify_user_request_created, notify_user_status_changed

ALLOWED_STATUSES = {"new", "in_progress", "done", "cancelled"}


async def create_request(session: AsyncSession, data: RequestCreate) -> Request:
    item = Request(
        title=data.title,
        description=data.description,
        tg_user_id=data.tg_user_id,
        tg_chat_id=data.tg_chat_id,
        status="new",
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)

    if item.tg_chat_id:
        notify_user_request_created.delay(item.tg_chat_id, item.id, item.title)

    return item


async def list_requests(
    session: AsyncSession,
    tg_user_id: int | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Request]:
    stmt = select(Request).order_by(Request.id.desc())
    if tg_user_id is not None:
        stmt = stmt.where(Request.tg_user_id == tg_user_id)
    if status is not None:
        stmt = stmt.where(Request.status == status)
    stmt = stmt.limit(limit).offset(offset)
    res = await session.execute(stmt)
    return list(res.scalars().all())


async def get_request_by_id(session: AsyncSession, request_id: int) -> Request | None:
    res = await session.execute(select(Request).where(Request.id == request_id))
    return res.scalar_one_or_none()


async def update_request_status(session: AsyncSession, item: Request, new_status: str) -> Request:
    if new_status not in ALLOWED_STATUSES:
        raise ValueError(f"Bad status: {new_status}. Allowed: {sorted(ALLOWED_STATUSES)}")

    await session.execute(update(Request).where(Request.id == item.id).values(status=new_status))
    await session.commit()

    refreshed = await get_request_by_id(session, item.id)
    if refreshed is None:
        return item

    if refreshed.tg_chat_id:
        notify_user_status_changed.delay(
            refreshed.tg_chat_id,
            refreshed.id,
            refreshed.title,
            refreshed.status,
        )

    return refreshed


async def stats_requests(session: AsyncSession) -> dict:
    res = await session.execute(select(Request.status, func.count(Request.id)).group_by(Request.status))
    items = res.all()
    return {"by_status": {status: int(cnt) for status, cnt in items}}
