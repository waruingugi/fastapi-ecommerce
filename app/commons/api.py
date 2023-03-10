from fastapi import APIRouter
from app.commons.routes import currency, country


router = APIRouter(prefix="/common")
router.include_router(currency.router, prefix="/currency", tags=["currencies"])
router.include_router(country.router, prefix="/country", tags=["country"])
