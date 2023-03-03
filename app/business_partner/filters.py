from fastapi_sqlalchemy_filter import Filter
from typing import Optional
from app.business_partner.models import BusinessPartner


class BusinessPartnerFilter(Filter):
    contact: Optional[str]
    email: Optional[str]

    class Constants(Filter.Constants):
        model = BusinessPartner
