import fastapi
from fastapi import Depends, Query
from app.core.deps import get_db
from app.business_partner.serializers.business_partner import BusinessPartnerInDBSerializer
from typing import Any
from sqlalchemy.orm import Session


router = fastapi.APIRouter()


@router.get("/business-partner", response_model=BusinessPartnerInDBSerializer)
async def read_business_partners(
    db: Session = Depends(get_db),
) -> Any:
    """Read business partners"""
    return{'business-partners': 'working on it...'}
