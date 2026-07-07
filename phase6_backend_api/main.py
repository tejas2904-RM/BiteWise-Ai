from __future__ import annotations

import os
import uvicorn

from backend.api.app import app
from backend.config import get_settings


def main() -> None:
    settings = get_settings()
    reload = os.getenv("RENDER") is None and os.getenv("API_RELOAD", "true").lower() == "true"
    uvicorn.run(
        "backend.api.app:app",
        host=str(settings["api_host"]),
        port=int(settings["api_port"]),
        reload=reload,
    )


if __name__ == "__main__":
    main()
