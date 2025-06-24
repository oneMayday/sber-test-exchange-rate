from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Query,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database.session_maker import session_maker
from .schemas import (
    ExchangeRateDeleteByCodeResponse,
    ExchangeRateGetAllDataInput,
    ExchangeRateGetAllDataResponse,
    CurrencyExchangeRatesSaveRequestInput,
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


@router.get(
    '/all-data',
    response_model=ExchangeRateGetAllDataResponse,
    responses={
        200: {"description": "Success"},
        500: {"description": "Internal server error"},
    },
)
async def get_currency_exchange_rates_all_data(
    pagination_input: ExchangeRateGetAllDataInput = Query(),
    session: AsyncSession = Depends(session_maker.session_dependency),
):
    """Getting all currency exchange rate data"""
    return await ExchangeRatesGetAllDataUseCase(session=session).execute(
        per_page=pagination_input.per_page,
        page=pagination_input.page
    )


@router.get(
    '/unique-currency-codes',
    response_model=list[str | None],
    responses={
            200: {"description": "Success"},
            500: {"description": "Internal server error"},
    },
)
async def get_unique_currency_codes(
    session: AsyncSession = Depends(session_maker.session_dependency)
):
    """Get unique currency codes"""
    return await CurrencyGetUniqueCodesUseCase(session=session).execute()


@router.post(
    '/currencies',
    response_model=CurrencyExchangeRatesSaveResponse,
    responses={
        200: {"description": "Records successfully deleted"},
        400: {"description": "Currency exchange rates already exists"},
        500: {"description": "Internal server error"},
        502: {"description": "Error when receiving data from the provider"},
    },
)
async def save_currency_exchange_rates(
    request_params: Annotated[CurrencyExchangeRatesSaveRequestInput, Body()],
    session: AsyncSession = Depends(session_maker.session_dependency),
):
    """Receiving currency exchange rate data from the provider and storing it"""
    return await CurrenciesExchangeRatesSaveUseCase(session=session, request_input=request_params).execute()


@router.delete(
    '/delete-by-code/{currency_code}',
    response_model=ExchangeRateDeleteByCodeResponse,
    responses={
        201: {"description": "Currency rates saved successfully"},
        400: {"description": "Invalid currency code format"},
        500: {"description": "Internal server error"},
    },
)
async def delete_currency_exchange_rates_by_code(
    session: AsyncSession = Depends(session_maker.session_dependency),
    currency_code: str = Depends(validate_currency_code)
) -> ExchangeRateDeleteByCodeResponse:
    """Deleting all records by currency code"""
    return await ExchangeRatesDeleteByCodeUseCase(session=session).execute(currency_code=currency_code)
