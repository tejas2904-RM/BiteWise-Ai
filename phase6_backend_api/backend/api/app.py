from __future__ import annotations

import backend.config  # noqa: F401 — register phase paths before contract imports

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.exceptions import register_exception_handlers
from backend.api.routes import router
from backend.config import get_settings

app = FastAPI(
    title="BiteWise API",
    description="Phase 6: Restaurant recommendation backend (Phases 1–5)",
    version="1.0.0",
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(router)
