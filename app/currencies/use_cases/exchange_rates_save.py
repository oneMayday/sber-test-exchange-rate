from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations import (
    FinancialDataBaseProvider,
    GetExchangeRateLitProviderResponse,
    GetExchangeRateProviderRequestParams,
    CentralBankRFProvider,
    ProviderExchangeRateInfo,
    ProviderCurrencyInfo,
)

from ..models import (
    Currency,
    ExchangeRate,
)
from ..model_services import (
    CurrencyModelService,
    ExchangeRateModelService,
)
from ..schemas import SaveCurrenciesExchangeRatesRequestInput


class SaveCurrenciesExchangeRatesUseCase:
    def __init__(
        self,
        session: AsyncSession,
        request_input: SaveCurrenciesExchangeRatesRequestInput,
        fin_data_provider: FinancialDataBaseProvider = None,
    ):
        self.session = session
        self.fin_data_provider = fin_data_provider or CentralBankRFProvider
        self.request_input = request_input
        self.currency_model_service = CurrencyModelService(self.session)
        self.exchange_rate_model_service = ExchangeRateModelService(self.session)

    async def execute(self):
        provider_data: GetExchangeRateLitProviderResponse = await self.fin_data_provider(
        ).get_currencies_exchange_rates(
            request_params=GetExchangeRateProviderRequestParams(**self.request_input.model_dump())
        )

        currencies_info: list[ProviderCurrencyInfo] = provider_data.currencies_info
        exchange_rates_info: list[ProviderExchangeRateInfo] = provider_data.exchange_rates_info

        currencies_to_save = [
            Currency(
                name=_.name,
                code=_.code
            ) for _ in currencies_info
        ]

        await self.currency_model_service.save_bulk(currencies=currencies_to_save)

        currencies = await self.currency_model_service.get_list()
        currencies_map = {_.code: _.id for _ in currencies}

        exchange_rates_to_save = []

        for _ in exchange_rates_info:
            base_currency_id = currencies_map.get(_.base_currency_code)
            quote_currency_id = currencies_map.get(_.quote_currency_code)
            rate = _.exchange_rate
            date = _.date

            if all([base_currency_id, quote_currency_id, rate]):
                exchange_rates_to_save.append(
                    ExchangeRate(
                        base_currency_id=base_currency_id,
                        quote_currency_id=quote_currency_id,
                        rate=rate,
                        date=date,
                    )
                )

        await self.exchange_rate_model_service.save_bulk(exchange_rates=exchange_rates_to_save)
        await self.session.commit()




