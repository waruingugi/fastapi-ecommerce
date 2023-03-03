from fastapi_sqlalchemy_filter import Filter
from app.business_partner.models import BusinessPartner


class BusinessPartnerFilter(Filter):
    search: str | None
    name: str | None
    email: str | None
    is_verified: bool | None

    class Constants(Filter.Constants):
        model = BusinessPartner
        search_model_fields = ["phone", "email"]
