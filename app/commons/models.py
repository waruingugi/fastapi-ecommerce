from app.db.base_class import Base
from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import mapped_column, relationship


class Currency(Base):
    name = mapped_column(String, unique=True)
    code = mapped_column(String, unique=True)


class Country(Base):
    dialing_code = mapped_column(String, unique=True)
    name = mapped_column(String, unique=True)
    iso2_code = mapped_column(String, unique=True)
    iso3_code = mapped_column(String, unique=True)
    currency_id = mapped_column(String, ForeignKey("currency.id"))

    currency = relationship("Currency", backref="country")

    def __repr__(self) -> str:
        return self.name
