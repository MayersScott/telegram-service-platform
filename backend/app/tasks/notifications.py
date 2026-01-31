from __future__ import annotations

import logging
import asyncio

import httpx

from app.core.config import settings
from app.tasks.celery_app import celery

logger = logging.getLogger(__name__)

STATUS_LABELS: dict[str, str] = {
    "new": "Новая",
    "in_progress": "В работе",
    "done": "Завершена",
    "cancelled": "Отменена",
}


def status_label(status: str) -> str:
    return STATUS_LABELS.get(status, status)


async def _send_telegram_message(chat_id: int, text: str) -> None:
    if not settings.bot_token:
        logger.warning("BOT_TOKEN is empty, skip telegram notify")
        return

    url = f"https://api.telegram.org/bot{settings.bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, json=payload)
        if r.status_code >= 400:
            logger.warning("Telegram sendMessage failed: %s %s", r.status_code, r.text)


@celery.task(name="notify_user_request_created")
def notify_user_request_created(chat_id: int, request_id: int, title: str) -> None:
    text = (
        "Заявка создана.\n"
        f"Номер: {request_id}\n"
        f"Тема: {title}\n"
        "Статус: Новая"
    )
    asyncio.run(_send_telegram_message(chat_id, text))


@celery.task(name="notify_user_status_changed")
def notify_user_status_changed(chat_id: int, request_id: int, title: str, status: str) -> None:
    text = (
        "Статус заявки изменён.\n"
        f"Номер: {request_id}\n"
        f"Тема: {title}\n"
        f"Новый статус: {status_label(status)}"
    )
    asyncio.run(_send_telegram_message(chat_id, text))
