from app.domains.users.users_api import router as users_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(users_router)
