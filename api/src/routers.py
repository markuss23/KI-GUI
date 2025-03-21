from fastapi import APIRouter

from api.src.roles.routers import router as roles_router
from api.src.categories.routers import router as categories_router

router = APIRouter()

router.include_router(roles_router)
router.include_router(categories_router)
