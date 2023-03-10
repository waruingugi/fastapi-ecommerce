from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.common.serializers.currency import (
    CurrencyCreateSerializer,
    CurrencyUpdateSerializer,
)
from app.common.models import Currency


class CurrencyDao(
    CRUDDao[Currency, CurrencyCreateSerializer, CurrencyUpdateSerializer]
):
    def get_or_create(
        self,
        db: Session,
        obj_in: CurrencyCreateSerializer,
    ) -> Currency:
        """Get a currency if it exists, otherwise create"""
        currency_obj = self.get(db, name=obj_in.name)

        if not currency_obj:
            currency_obj = self.create(db, obj_in=obj_in)

        return currency_obj


currency_dao = CurrencyDao(Currency)
