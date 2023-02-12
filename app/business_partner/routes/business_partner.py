import fastapi
from fastapi import Depends, Query
from app.core.deps import get_db
from app.business_partner.serializers.business_partner import (
    BusinessPartnerInDBSerializer,
    BusinessPartnerCreateSerializer,
    BusinessPartnerCreateExistingOwnerSerializer
)
from typing import Any
from sqlalchemy.orm import Session
from app.business_partner.daos.business_partner import business_partner_dao
from typing import List
from app.exceptions.custom import HttpErrorException
from app.errors.custom import ErrorCodes
from http import HTTPStatus
from app.users.daos.user import user_dao


router = fastapi.APIRouter()


@router.get("/business-partner", response_model=List[BusinessPartnerInDBSerializer])
async def read_business_partners(
    db: Session = Depends(get_db),
) -> Any:
    """Read business partners"""
    return business_partner_dao.get_all(db)


@router.post("/business-partner", response_model=BusinessPartnerInDBSerializer)
async def create_business_partner(
    business_data: BusinessPartnerCreateSerializer,
    db: Session = Depends(get_db)
) -> Any:
    """Create business partner"""
    business_data_dict = business_data.dict(exclude_unset=True)
    owner = business_data_dict.pop("owner")

    user_in = user_dao.get_by_phone_or_email(
        db, email=owner.get("email", None), phone=owner.get("phone", None)
    )

    if not user_in:
        raise HttpErrorException(
            status_code=HTTPStatus.BAD_REQUEST,
            error_code=ErrorCodes.BUSINESS_OWNER_DOES_NOT_EXIST.name,
            error_message=ErrorCodes.BUSINESS_OWNER_DOES_NOT_EXIST.value
        )

    obj_in = BusinessPartnerCreateExistingOwnerSerializer(
        owner_id=user_in.id, **business_data_dict
    )

    return business_partner_dao.get_or_create(db, obj_in=obj_in)
