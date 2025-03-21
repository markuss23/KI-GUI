from fastapi import APIRouter

from api.src.roles.routers import router as roles_router

router = APIRouter()

router.include_router(roles_router)
