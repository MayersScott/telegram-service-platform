from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.init_db import ensure_admin_user


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Telegram Service Platform",
        version="0.1.0",
        debug=settings.env == "dev",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    @app.on_event("startup")
    async def _startup() -> None:
        await ensure_admin_user()

    return app


app = create_app()
