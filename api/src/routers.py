from fastapi import APIRouter

from api.src.roles.routers import router as roles_router
from api.src.categories.routers import router as categories_router
from api.src.courses.routers import router as courses_router
from api.src.users.routers import router as users_router

router = APIRouter()

router.include_router(roles_router)
router.include_router(users_router)
router.include_router(categories_router)
router.include_router(courses_router)
