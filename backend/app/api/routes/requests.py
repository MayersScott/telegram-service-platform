from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin
from app.db.session import get_session
from app.schemas.request import RequestCreate, RequestOut, RequestUpdateStatus
from app.services.requests import (
    create_request,
    list_requests,
    get_request_by_id,
    update_request_status,
    stats_requests,
)

router = APIRouter()


@router.post("/", response_model=RequestOut)
async def create(req: RequestCreate, session: AsyncSession = Depends(get_session)) -> RequestOut:
    item = await create_request(session, req)
    return RequestOut.model_validate(item)


@router.get("/my", response_model=list[RequestOut])
async def my_requests(
    tg_user_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(get_session),
) -> list[RequestOut]:
    items = await list_requests(session, tg_user_id=tg_user_id)
    return [RequestOut.model_validate(x) for x in items]


@router.get("/", response_model=list[RequestOut])
async def admin_list(
    status: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
    _admin=Depends(get_current_admin),
) -> list[RequestOut]:
    items = await list_requests(session, status=status, limit=limit, offset=offset)
    return [RequestOut.model_validate(x) for x in items]


@router.get("/stats", response_model=dict)
async def admin_stats(
    session: AsyncSession = Depends(get_session),
    _admin=Depends(get_current_admin),
) -> dict:
    return await stats_requests(session)


@router.patch("/{request_id}/status", response_model=RequestOut)
async def admin_update_status(
    request_id: int,
    data: RequestUpdateStatus,
    session: AsyncSession = Depends(get_session),
    _admin=Depends(get_current_admin),
) -> RequestOut:
    item = await get_request_by_id(session, request_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Not found")
    try:
        item = await update_request_status(session, item, data.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return RequestOut.model_validate(item)
