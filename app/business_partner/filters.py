from fastapi_sqlalchemy_filter import Filter, FilterDepends, with_prefix
from app.business_partner.models import BusinessPartner
from app.users.filters import UserBaseFilter


class BusinessPartnerBaseFilter(Filter):
    contact: str | None

    class Constants(Filter.Constants):
        model = BusinessPartner
        search_field_name = "contact"
        search_model_fields = ["phone", "email"]


class BusinessPartnerFilter(BusinessPartnerBaseFilter, Filter):
    name: str | None
    is_verified: bool | None
    owner: UserBaseFilter | None = FilterDepends(with_prefix("owner", UserBaseFilter))
