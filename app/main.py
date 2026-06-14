from fastapi import FastAPI

from app.core.config import settings
from app.core.lifespan import lifespan


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {
        "message": "OneTapGOV Backend Running"
    }