from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db

from backend.app.modules.auth.dependencies import (
    get_current_user,
)

from backend.app.modules.profile.repository import (
    ProfileRepository,
)
from backend.app.modules.education.repository import (
    EducationRepository,
)
from backend.app.modules.women.repository import (
    WomenRepository,
)
from backend.app.modules.agriculture.repository import (
    AgricultureRepository,
)
from backend.app.modules.documents.repository import (
    DocumentRepository,
)
from backend.app.modules.schemes.repository import (
    SchemeRepository,
)

from backend.app.modules.recommendation.schemas import (
    SchemeRecommendationResponse,
)
from backend.app.modules.recommendation.service import (
    RecommendationService,
)

router = APIRouter()


@router.get(
    "",
    response_model=list[
        SchemeRecommendationResponse
    ],
)
async def get_recommendations(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = RecommendationService(
        scheme_repository=SchemeRepository(db),
        profile_repository=ProfileRepository(db),
        education_repository=EducationRepository(db),
        women_repository=WomenRepository(db),
        agriculture_repository=AgricultureRepository(db),
        document_repository=DocumentRepository(db),
    )

    return await service.get_recommendations(
        current_user
    )