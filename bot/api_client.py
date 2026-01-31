from __future__ import annotations

from typing import Any

import httpx

from config import bot_settings


class APIClient:
    def __init__(self) -> None:
        self.base_url = bot_settings.api_base_url.rstrip("/")

    async def upsert_user(self, tg_user_id: int, tg_chat_id: int) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                f"{self.base_url}/public/telegram/upsert",
                json={"tg_user_id": tg_user_id, "tg_chat_id": tg_chat_id},
            )
            r.raise_for_status()
            return r.json()

    async def create_request(
        self,
        title: str,
        description: str | None,
        tg_user_id: int,
        tg_chat_id: int,
    ) -> dict[str, Any]:
        payload = {
            "title": title,
            "description": description,
            "tg_user_id": tg_user_id,
            "tg_chat_id": tg_chat_id,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(f"{self.base_url}/requests/", json=payload)
            r.raise_for_status()
            return r.json()

    async def list_my_requests(self, tg_user_id: int) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/requests/my", params={"tg_user_id": tg_user_id})
            r.raise_for_status()
            return r.json()
