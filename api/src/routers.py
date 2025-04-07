from fastapi import APIRouter

from api.src.roles.routers import router as roles_router
from api.src.categories.routers import router as categories_router
from api.src.courses.routers import router as courses_router
from api.src.users.routers import router as users_router
from api.src.tasks.routers import router as tasks_router
from api.src.enrollments.routers import router as enrollments_router
from api.src.task_completions.routers import router as task_completions_router

"""
Tento soubor definuje router pro FastAPI aplikaci.
Router je použit pro organizaci endpointů do modulárních částí.
Každý modul má svůj vlastní router, který obsahuje definici endpointů pro danou část aplikace.
"""


router = APIRouter()

router.include_router(roles_router)
router.include_router(users_router)
router.include_router(categories_router)
router.include_router(courses_router)
router.include_router(tasks_router)
router.include_router(enrollments_router)
router.include_router(task_completions_router)
