from app.domains.cards.cards_api import router as cards_router
from app.domains.users.users_api import router as users_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(users_router)
router.include_router(cards_router)
