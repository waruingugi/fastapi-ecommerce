from fastapi_sqlalchemy_filter import Filter, FilterDepends, with_prefix
from app.business_partner.models import BusinessPartner
from app.users.filters import UserBaseFilter
from app.commons.filters import CountryFilter
from typing import List
from pydantic import Field


class BusinessPartnerBaseFilter(Filter):
    contact: str | None

    class Constants(Filter.Constants):
        model = BusinessPartner
        search_field_name = "contact"
        search_model_fields = ["phone", "email"]


class BusinessPartnerFilter(BusinessPartnerBaseFilter):
    name__ilike: str | None = Field(alias="name")
    is_verified: bool | None
    owner: UserBaseFilter | None = FilterDepends(with_prefix("owner", UserBaseFilter))
    country: CountryFilter | None = FilterDepends(with_prefix("country", CountryFilter))
    order_by: List[str] | None
