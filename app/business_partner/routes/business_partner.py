from fastapi import Depends, APIRouter
from app.core.deps import (
    get_db,
    Permissions,
    get_current_active_user,
    RestrictBusinessPartnerFilter,
)
from app.business_partner.serializers.business_partner import (
    BusinessPartnerInDBSerializer,
    BusinessPartnerCreateExistingOwnerSerializer,
    BusinessPartnerUpdateSerializer,
)
from typing import Any
from sqlalchemy.orm import Session
from app.business_partner.daos.business_partner import business_partner_dao
from typing import List
from app.users.daos.user import user_dao
from app.users.models import User
from app.core.logger import LoggingRoute
from app.business_partner.filters import BusinessPartnerFilter
from fastapi_sqlalchemy_filter import FilterDepends
from app.users.constants import UserTypes
from app.business_partner.permissions import BusinessPartnerPermissions
from fastapi_pagination import Params

router = APIRouter(route_class=LoggingRoute)


@router.get("/business-partner", response_model=List[BusinessPartnerInDBSerializer])
async def read_business_partners(
    params: Params = Depends(),
    bp_filter: BusinessPartnerFilter = FilterDepends(BusinessPartnerFilter),
    db: Session = Depends(get_db),
    _: Permissions = Depends(
        Permissions(BusinessPartnerPermissions.business_partner_list)
    ),
    restrict_bp_filter: RestrictBusinessPartnerFilter = Depends(
        RestrictBusinessPartnerFilter
    ),
) -> Any:
    """Read business partners"""
    bp_filter_dict = bp_filter.dict()
    search_filter = restrict_bp_filter(search_filter=bp_filter)

    if not any(bp_filter_dict.values()):  # Returns True if all values are falsy/None
        return business_partner_dao.get_multi_paginated(db, bp_filter, params)

    return business_partner_dao.search(db, search_filter)


@router.post("/business-partner", response_model=BusinessPartnerInDBSerializer)
async def create_business_partner(
    bp_in: BusinessPartnerCreateExistingOwnerSerializer,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> Any:
    """Create business partner"""
    owner = user_dao.get_not_none(
        db, id=bp_in.owner_id
    )  # Assert that the bp owner exists
    new_bp = business_partner_dao.get_or_create(db, obj_in=bp_in)

    user_dao.update(
        db, db_obj=owner, obj_in={"user_type": UserTypes.BUSINESS_OWNER.value}
    )  # Update user to BUSINESS_OWNER type
    return new_bp


@router.patch(
    "/business-partner/{busineess_partner_id}",
    response_model=BusinessPartnerInDBSerializer,
)
async def update_business_partner(
    business_partner_id: str,
    bp_in: BusinessPartnerUpdateSerializer,
    db: Session = Depends(get_db),
    _: Permissions = Depends(
        Permissions(BusinessPartnerPermissions.business_partner_update)
    ),
) -> Any:
    """Update business partner"""
    # Check whether the business owner exists
    if bp_in.owner_id:
        user_dao.get_not_none(db, id=bp_in.owner_id)

    # Get the business_partner to be updated
    db_obj = business_partner_dao.get_not_none(db, id=business_partner_id)

    return business_partner_dao.update(
        db, db_obj=db_obj, obj_in=bp_in.dict(exclude_unset=True)
    )
