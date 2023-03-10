from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.common.serializers.country import (
    CountryCreateSerializer,
    CountryUpdateSerializer,
)
from app.common.models import Country


class CountryDao(CRUDDao[Country, CountryCreateSerializer, CountryUpdateSerializer]):
    def get_or_create(
        self,
        db: Session,
        obj_in: CountryCreateSerializer,
    ) -> Country:
        """Get a country if it exists, otherwise create"""
        country_obj = self.get(db, name=obj_in.name)

        if not country_obj:
            country_obj = self.create(db, obj_in=obj_in)

        return country_obj


country_dao = CountryDao(Country)
