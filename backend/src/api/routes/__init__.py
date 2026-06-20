from fastapi import APIRouter
from src.api.routes import upload,query


router = APIRouter()

router.include_router(upload.router,prefix="/upload",tags=["Upload"])
router.include_router(query.router,prefix="/query",tags=["Query"])