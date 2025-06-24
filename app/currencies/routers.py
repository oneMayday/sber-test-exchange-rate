from typing import Annotated

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database.session_maker import session_maker
from .schemas import (
    ExchangeRateDeleteByCodeResponse,
    ExchangeRateGetAllDataInput,
    ExchangeRateGetAllDataResponse,
    CurrencysExchangeRatesSaveRequestInput,
    CurrencyExchangeRatesSaveResponse
)
from .use_cases import (
    ExchangeRatesGetAllDataUseCase,
    ExchangeRatesDeleteByCodeUseCase,
    CurrencyGetUniqueCodesUseCase,
    CurrenciesExchangeRatesSaveUseCase
)

from .utils import validate_currency_code

router = APIRouter()


@router.get('/all-data', response_model=ExchangeRateGetAllDataResponse)
async def get_currency_exchange_rates_all_data(
    pagination_input: ExchangeRateGetAllDataInput = Query(),
    session: AsyncSession = Depends(session_maker.session_dependency),
):
    """Получение всех данных о курсах валют"""
    return await ExchangeRatesGetAllDataUseCase(session=session).execute(
        per_page=pagination_input.per_page,
        page=pagination_input.page
    )


@router.get('/unique-currency-codes', response_model=list[str | None])
async def get_unique_currency_codes(
    session: AsyncSession = Depends(session_maker.session_dependency)
):
    """Получение списка уникальных кодов валют."""
    return await CurrencyGetUniqueCodesUseCase(session=session).execute()


@router.post('/currencies', response_model=CurrencyExchangeRatesSaveResponse)
async def save_currency_exchange_rates(
    request_params: Annotated[CurrencysExchangeRatesSaveRequestInput, Query()],
    session: AsyncSession = Depends(session_maker.session_dependency),
):
    """Получение данных о курсах валют от провайдера и их сохранение"""
    return await CurrenciesExchangeRatesSaveUseCase(session=session, request_input=request_params).execute()


@router.delete(
    '/delete-by-code/{currency_code}',
    responses={
        200: {"description": "Records successfully deleted"},
        400: {"description": "Invalid currency code format"}
    }
)
async def delete_currency_exchange_rates_by_code(
    session: AsyncSession = Depends(session_maker.session_dependency),
    currency_code: str = Depends(validate_currency_code)
) -> ExchangeRateDeleteByCodeResponse:
    """Удаление всех записей по коду валюты"""
    return await ExchangeRatesDeleteByCodeUseCase(session=session).execute(currency_code=currency_code)
