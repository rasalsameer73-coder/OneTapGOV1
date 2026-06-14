from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Database Engine (create only if DATABASE_URL is set to avoid import-time errors)
engine = None
if settings.DATABASE_URL:
    try:
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
        )
    except Exception:
        engine = None


# Session Factory
AsyncSessionLocal = None
if engine is not None:
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


# Base Model
class Base(DeclarativeBase):
    pass


# Dependency
async def get_db():
    if AsyncSessionLocal is None:
        raise RuntimeError("AsyncSessionLocal is not configured. Set DATABASE_URL to enable DB access.")
    async with AsyncSessionLocal() as session:
        yield session