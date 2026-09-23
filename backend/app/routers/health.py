from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "personalized-healthcare-assistant",
        "llm_provider": settings.llm_provider,
    }
