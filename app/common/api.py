from fastapi import APIRouter
from app.common.routes import currency


router = APIRouter(prefix="/currency", tags=["currencies"])
router.include_router(currency.router)
