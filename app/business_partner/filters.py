from fastapi_sqlalchemy_filter import Filter, FilterDepends, with_prefix
from app.business_partner.models import BusinessPartner

from app.users.filters import UserFilter


class BusinessPartnerFilter(Filter):
    search: str | None
    name: str | None
    is_verified: bool | None

    owner: UserFilter | None = FilterDepends(with_prefix("owner", UserFilter))

    class Constants(Filter.Constants):
        model = BusinessPartner
        search_model_fields = ["phone", "email"]
