from fastapi import FastAPI

from orchestrator.api.routes import router
from orchestrator.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Multi-repo Smart Test Orchestrator",
)

app.include_router(router)
