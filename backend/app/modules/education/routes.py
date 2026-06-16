from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.modules.auth.dependencies import get_current_user
from backend.app.modules.education.repository import EducationRepository
from backend.app.modules.education.schemas import (
    EducationProfileCreate,
    EducationProfileUpdate,
    EducationProfileResponse,
)
from backend.app.modules.education.service import EducationService


router = APIRouter()


@router.post(
    "",
    response_model=EducationProfileResponse,
)
async def create_education_profile(
    profile_data: EducationProfileCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = EducationRepository(db)

    service = EducationService(repository)

    return await service.create_education_profile(
        current_user,
        profile_data,
    )


@router.get(
    "",
    response_model=EducationProfileResponse,
)
async def get_education_profile(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = EducationRepository(db)

    service = EducationService(repository)

    return await service.get_education_profile(
        current_user
    )


@router.put(
    "",
    response_model=EducationProfileResponse,
)
async def update_education_profile(
    profile_data: EducationProfileUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = EducationRepository(db)

    service = EducationService(repository)

    return await service.update_education_profile(
        current_user,
        profile_data,
    )