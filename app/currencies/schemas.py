from datetime import date as _date
from decimal import Decimal

from pydantic import BaseModel, Field

from app.utils import PaginationInput, PaginationResponse


class CurrencyExchangeRate(BaseModel):
    id: int
    code: str
    rate: Decimal
    date: _date


class CurrencyExchangeRatesSaveRequestInput(BaseModel):
    date: _date = Field(examples=["2025-06-24"])


class CurrencyExchangeRatesSaveResponse(BaseModel):
    message: str = "Currency rates saved successfully"


class ExchangeRateDeleteByCodeResponse(BaseModel):
    message: str


class ExchangeRateGetAllDataInput(PaginationInput):
    pass


class ExchangeRateGetAllDataResponse(PaginationResponse):
    items: list[CurrencyExchangeRate]


