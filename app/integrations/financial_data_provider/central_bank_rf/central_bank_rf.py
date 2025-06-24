from aiohttp import ClientSession
from dateutil import parser
from typing import NoReturn

from app.integrations import (
    FinancialDataBaseProvider,
    GetExchangeRateProviderRequestParams,
    GetExchangeRateLitProviderResponse,
    ProviderCurrencyInfo,
    ProviderExchangeRateInfo,
)
from .exceptions import CentraBankProviderResponseException


class CentralBankRFProvider(FinancialDataBaseProvider):
    """Провайдер ЦБ РФ."""

    provider_name = "ЦБ РФ"
    provider_url = "https://www.cbr-xml-daily.ru"

    async def get_currencies_exchange_rates(
        self,
        request_params: GetExchangeRateProviderRequestParams
    ) -> GetExchangeRateLitProviderResponse | NoReturn:
        request_url = self.provider_url + "/daily_json.js"

        date = request_params.date.strftime("%Y-%m-%d")

        try:
            async with ClientSession() as session:
                params = {
                    'date_req': date
                }
                async with session.get(request_url, params=params) as response:
                    data = await response.json(content_type=None)

                    out = GetExchangeRateLitProviderResponse()
                    default_currency_info = self.get_default_currency_info()
                    out.currencies_info.append(default_currency_info)

                    default_currency_code = default_currency_info.code
                    default_currency_name = default_currency_info.name

                    currencies_data = data["Valute"]
                    string_date = data["Date"]
                    datetime_object = parser.parse(string_date)
                    date = datetime_object.date()

                    for currency, exchange_rate_data in currencies_data.items():
                        code = exchange_rate_data["CharCode"]
                        name = exchange_rate_data["Name"]
                        exchange_rate = exchange_rate_data["Value"]

                        currency_info = ProviderCurrencyInfo(
                            code=code,
                            name=name,
                        )
                        exchange_rate_info = ProviderExchangeRateInfo(
                            base_currency_code=default_currency_code,
                            base_currency_name=default_currency_name,
                            quote_currency_code=code,
                            quote_currency_name=name,
                            exchange_rate=exchange_rate,
                            date=date
                        )
                        out.currencies_info.append(currency_info)
                        out.exchange_rates_info.append(exchange_rate_info)
                    return out
        except Exception as ex:
            raise CentraBankProviderResponseException

    @staticmethod
    def get_default_currency_info() -> ProviderCurrencyInfo:
        return ProviderCurrencyInfo(code='RUB', name='Российский рубль')
