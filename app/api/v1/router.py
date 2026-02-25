from fastapi import APIRouter

from app.domains.alerts.alert_api import router as alerts_router
from app.domains.cards.cards_api import router as cards_router
from app.domains.merchants.merchant_api import router as merchants_router
from app.domains.transactions.transactions_api import router as transactions_router
from app.domains.users.users_api import router as users_router

router = APIRouter()
router.include_router(users_router)
router.include_router(cards_router)
router.include_router(merchants_router)
router.include_router(transactions_router)
router.include_router(alerts_router)
