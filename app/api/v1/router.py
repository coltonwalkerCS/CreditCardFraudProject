from fastapi import APIRouter

from app.domains.cards.cards_api import router as cards_router
from app.domains.merchants.merchant_api import router as merchant_router
from app.domains.users.users_api import router as users_router

router = APIRouter()
router.include_router(users_router)
router.include_router(cards_router)
router.include_router(merchant_router)
