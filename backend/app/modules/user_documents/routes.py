from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db

from backend.app.modules.auth.dependencies import (
    get_current_user,
)

from backend.app.modules.user_documents.repository import (
    UserDocumentRepository,
)

from backend.app.modules.user_documents.schemas import (
    UserDocumentCreate,
    UserDocumentResponse,
)

from backend.app.modules.user_documents.service import (
    UserDocumentService,
)

router = APIRouter()


@router.post(
    "",
    response_model=UserDocumentResponse,
)
async def upload_document(
    document_data: UserDocumentCreate,
    current_user=Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(
        get_db
    ),
):

    repository = UserDocumentRepository(
        db
    )

    service = UserDocumentService(
        repository
    )

    return await service.create_document(
        current_user,
        document_data,
    )


@router.get(
    "",
    response_model=list[
        UserDocumentResponse
    ],
)
async def get_user_documents(
    current_user=Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(
        get_db
    ),
):

    repository = UserDocumentRepository(
        db
    )

    service = UserDocumentService(
        repository
    )

    return await service.get_user_documents(
        current_user
    )