from app.core.deps import get_db, Permissions
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.commons.serializers.country import (
    CountryCreateSerializer,
    CountryUpdateSerializer,
    CountryInDBSerializer,
)
from typing import List
from app.commons.daos.country import country_dao
from app.commons.daos.currency import currency_dao
from app.core.logger import LoggingRoute
from app.commons.permissions import CountryPermissions
from app.commons.filters import CountryFilter
from fastapi_sqlalchemy_filter import FilterDepends
from typing import Any

router = APIRouter(route_class=LoggingRoute)


@router.post("/", response_model=CountryInDBSerializer)
async def create_country(
    country_in: CountryCreateSerializer,
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(CountryPermissions.country_create)),
) -> Any:
    """Create country"""
    currency_dao.get_not_none(db, id=country_in.currency_id)

    return country_dao.get_or_create(db, obj_in=country_in)


@router.get("/", response_model=List[CountryInDBSerializer])
async def read_countries(
    country_filter: CountryFilter = FilterDepends(CountryFilter),
    db: Session = Depends(get_db),
) -> Any:
    """Read countries"""
    country_filter_dict = country_filter.dict()

    if not any(
        country_filter_dict.values()
    ):  # Returns True if all values are falsy/None
        return country_dao.get_all(db)

    return country_dao.search(db, country_filter)


@router.patch("/{country_id}", response_model=CountryInDBSerializer)
async def update_country(
    country_id: str,
    country_in: CountryUpdateSerializer,
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(CountryPermissions.country_update)),
) -> Any:
    """Update country"""
    db_obj = country_dao.get_not_none(db, id=country_id)

    return country_dao.update(db, db_obj=db_obj, obj_in=country_in)
