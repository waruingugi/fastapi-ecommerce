from fastapi import APIRouter
from app.business_partner.routes import business_partner


router = APIRouter(prefix="/business_partner", tags=["business partners"])
router.include_router(business_partner.router)
