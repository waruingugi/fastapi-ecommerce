from fastapi import Depends, APIRouter
from app.core.deps import get_db
from app.business_partner.serializers.business_partner import (
    BusinessPartnerInDBSerializer,
    BusinessPartnerCreateSerializer,
    BusinessPartnerCreateExistingOwnerSerializer,
)
from typing import Any
from sqlalchemy.orm import Session
from app.business_partner.daos.business_partner import business_partner_dao
from typing import List
from app.users.daos.user import user_dao
from app.core import deps
from app.users.models import User
from app.core.logger import LoggingRoute
from app.business_partner.filters import BusinessPartnerFilter
from fastapi_sqlalchemy_filter import FilterDepends

router = APIRouter(route_class=LoggingRoute)


@router.get("/business-partner", response_model=List[BusinessPartnerInDBSerializer])
async def read_business_partners(
    bp_filter: BusinessPartnerFilter = FilterDepends(BusinessPartnerFilter),
    db: Session = Depends(get_db),
    _: User = Depends(deps.get_current_active_user),
) -> Any:
    """Read business partners"""

    """Read user roles"""
    bp_filter_dict = bp_filter.dict()
    import pdb

    pdb.set_trace()

    if not any(bp_filter_dict.values()):  # Returns True if all values are falsy/None
        return business_partner_dao.get_all(db)

    return business_partner_dao.search(db, bp_filter)


@router.post("/business-partner", response_model=BusinessPartnerInDBSerializer)
async def create_business_partner(
    business_data: BusinessPartnerCreateSerializer, db: Session = Depends(get_db)
) -> Any:
    """Create business partner"""
    business_data_dict = business_data.dict(exclude_unset=True)

    """Check whether the business owner exists"""
    user_in = user_dao.get_or_create(db, obj_in=business_data.owner)

    obj_in = BusinessPartnerCreateExistingOwnerSerializer(
        owner_id=user_in.id, **business_data_dict
    )

    return business_partner_dao.get_or_create(db, obj_in=obj_in)
