from datetime import date
from decimal import Decimal
from typing import List

from sqlalchemy import (
    DECIMAL,
    Date,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship,
)

from app.models import BaseModel


class Currency(BaseModel):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String, unique=True)
    exchange_rates_base: Mapped[List["ExchangeRate"]] = relationship("ExchangeRate", foreign_keys="ExchangeRate.base_currency_id", back_populates="base_currency")
    exchange_rates_quote: Mapped[List["ExchangeRate"]] = relationship("ExchangeRate", foreign_keys="ExchangeRate.quote_currency_id", back_populates="quote_currency")


class ExchangeRate(BaseModel):
    __tablename__ = "exchange_rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    quote_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    rate: Mapped[Decimal] = mapped_column(DECIMAL(precision=8, decimal_return_scale=2))
    date: Mapped[date] = mapped_column(Date)
    base_currency: Mapped[Currency] = relationship("Currency", foreign_keys=[base_currency_id], back_populates="exchange_rates_base")
    quote_currency: Mapped[Currency] = relationship("Currency", foreign_keys=[quote_currency_id], back_populates="exchange_rates_quote")