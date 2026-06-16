from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from backend.app.core.database import (
    get_db,
)

from backend.app.modules.auth.dependencies import (
    get_current_user,
)

from backend.app.modules.documents.repository import (
    DocumentRepository,
)

from backend.app.modules.user_documents.repository import (
    UserDocumentRepository,
)

from backend.app.modules.readiness.schemas import (
    ReadinessResponse,
)

from backend.app.modules.readiness.service import (
    ReadinessService,
)

router = APIRouter()


@router.get(
    "/{scheme_id}/{scheme_name}",
    response_model=ReadinessResponse,
)
async def get_readiness(
    scheme_id: int,
    scheme_name: str,
    current_user=Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(
        get_db
    ),
):

    service = ReadinessService(
        document_repository=DocumentRepository(
            db
        ),

        user_document_repository=UserDocumentRepository(
            db
        ),
    )

    return await service.get_readiness(
        current_user,
        scheme_id,
        scheme_name,
    )