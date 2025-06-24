from typing import NoReturn

from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations import (
    FinancialDataBaseProvider,
    GetExchangeRateLitProviderResponse,
    GetExchangeRateProviderRequestParams,
    CentralBankRFProvider,
    ProviderExchangeRateInfo,
    ProviderCurrencyInfo,
)
from ..exceptions import ExchangeRatesAlreadyExistsException
from ..models import (
    Currency,
    ExchangeRate,
)
from ..model_services import (
    CurrencyModelService,
    ExchangeRateModelService,
)
from ..schemas import (
    CurrencysExchangeRatesSaveRequestInput,
    CurrencyExchangeRatesSaveResponse,
)


class CurrenciesExchangeRatesSaveUseCase:
    def __init__(
        self,
        session: AsyncSession,
        request_input: CurrencysExchangeRatesSaveRequestInput,
        fin_data_provider: FinancialDataBaseProvider = None,
    ):
        self.session = session
        self.fin_data_provider = fin_data_provider or CentralBankRFProvider
        self.request_input = request_input
        self.currency_model_service = CurrencyModelService(self.session)
        self.exchange_rate_model_service = ExchangeRateModelService(self.session)

    async def execute(self) -> CurrencyExchangeRatesSaveResponse | NoReturn:
        # Проверяем, что курсы за указанную дату существуют.
        await self.check_is_target_date_exchange_rate_exists()

        # Если в БД записей нет - делаем запрос провайдеру
        provider_data: GetExchangeRateLitProviderResponse = await self.fin_data_provider(
        ).get_currencies_exchange_rates(
            request_params=GetExchangeRateProviderRequestParams(**self.request_input.model_dump())
        )

        currencies_info: list[ProviderCurrencyInfo] = provider_data.currencies_info
        exchange_rates_info: list[ProviderExchangeRateInfo] = provider_data.exchange_rates_info

        # Сохраняем валюты и курсы валют
        await self.save_missing_currencies(currencies_info=currencies_info)
        await self.save_missing_exchange_rates(exchange_rates_info=exchange_rates_info)

        return CurrencyExchangeRatesSaveResponse()

    async def check_is_target_date_exchange_rate_exists(self):
        existing_exchange_rates = await self.exchange_rate_model_service.get_list_by_target_date(
            target_date=self.request_input.date
        )

        if existing_exchange_rates:
            raise ExchangeRatesAlreadyExistsException

    async def save_missing_currencies(self, currencies_info: list[ProviderCurrencyInfo]):
        """Создание валют, которых нет в БД, но есть в ответе от провайдера."""
        existing_currencies = await self.currency_model_service.get_list()

        existing_currencies_map = {_.code: _.id for _ in existing_currencies}

        currencies_to_save = [
            Currency(
                name=_.name,
                code=_.code
            ) for _ in currencies_info if _.code not in existing_currencies_map.keys()
        ]

        if currencies_to_save:
            await self.currency_model_service.save_bulk(currencies=currencies_to_save)

    async def save_missing_exchange_rates(self, exchange_rates_info: list[ProviderExchangeRateInfo]):
        """Создание валют, которых нет в БД, но есть в ответе от провайдера."""
        existing_currencies = await self.currency_model_service.get_list()

        existing_currencies_map = {_.code: _.id for _ in existing_currencies}

        exchange_rates_to_save = []

        for _ in exchange_rates_info:
            base_currency_id = existing_currencies_map.get(_.base_currency_code)
            quote_currency_id = existing_currencies_map.get(_.quote_currency_code)
            rate = _.exchange_rate
            date = _.date

            if all([base_currency_id, quote_currency_id, rate, date]):
                exchange_rates_to_save.append(
                    ExchangeRate(
                        base_currency_id=base_currency_id,
                        quote_currency_id=quote_currency_id,
                        rate=rate,
                        date=date,
                    )
                )

        if exchange_rates_to_save:
            await self.exchange_rate_model_service.save_bulk(exchange_rates=exchange_rates_to_save)
