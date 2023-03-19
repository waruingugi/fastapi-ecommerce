from app.core.deps import get_db, Permissions, get_current_active_superuser
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.commons.serializers.currency import (
    CurrencyCreateSerializer,
    CurrencyUpdateSerializer,
    CurrencyInDBSerializer,
)
from typing import List
from app.commons.daos.currency import currency_dao
from app.core.logger import LoggingRoute
from app.commons.permissions import CurrencyPermissions
from app.commons.filters import CurrencyFilter
from fastapi_sqlalchemy_filter import FilterDepends
from typing import Any
from app.users.models import User

router = APIRouter(route_class=LoggingRoute)


@router.post("/", response_model=CurrencyInDBSerializer)
async def create_currency(
    currency_in: CurrencyCreateSerializer,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_superuser),
) -> Any:
    """Create currency"""
    return currency_dao.get_or_create(db, obj_in=currency_in)


@router.get("/", response_model=List[CurrencyInDBSerializer])
async def read_currencies(
    currency_filter: CurrencyFilter = FilterDepends(CurrencyFilter),
    db: Session = Depends(get_db),
) -> Any:
    """Read currencies"""
    currency_filter_dict = currency_filter.dict()

    if not any(
        currency_filter_dict.values()
    ):  # Returns True if all values are falsy/None
        return currency_dao.get_all(db)

    return currency_dao.search(db, currency_filter)


@router.patch("/{currency_id}", response_model=CurrencyInDBSerializer)
async def update_currency(
    currency_id: str,
    currency_in: CurrencyUpdateSerializer,
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(CurrencyPermissions.currency_update)),
) -> Any:
    """Update currency"""
    db_obj = currency_dao.get_not_none(db, id=currency_id)

    return currency_dao.update(db, db_obj=db_obj, obj_in=currency_in)
