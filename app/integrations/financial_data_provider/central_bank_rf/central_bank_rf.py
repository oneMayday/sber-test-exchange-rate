import xml.etree.ElementTree as ET

from aiohttp import ClientSession
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
    provider_url = "http://www.cbr.ru/"

    async def get_currencies_exchange_rates(
        self,
        request_params: GetExchangeRateProviderRequestParams
    ) -> GetExchangeRateLitProviderResponse | NoReturn:
        request_url = self.provider_url + "scripts/XML_daily.asp"

        date = request_params.date.strftime("%Y-%m-%d")
        url_date = request_params.date.strftime("%d/%m/%Y")
        url_params = {'date_req': url_date}

        out = GetExchangeRateLitProviderResponse()
        default_currency_info = self.get_default_currency_info()
        out.currencies_info.append(default_currency_info)
        default_currency_code = default_currency_info.code
        default_currency_name = default_currency_info.name

        try:
            async with ClientSession() as session:
                async with session.get(request_url, params=url_params) as response:
                    data = await response.read()
                    tree = ET.fromstring(data)

                    for _ in tree.findall("Valute"):
                        code = _.find("CharCode").text
                        name = _.find("Name").text
                        exchange_rate = _.find("Value").text

                        if code and name and exchange_rate:
                            currency_info = ProviderCurrencyInfo(
                                code=code,
                                name=name,
                            )
                            exchange_rate_info = ProviderExchangeRateInfo(
                                base_currency_code=default_currency_code,
                                base_currency_name=default_currency_name,
                                quote_currency_code=code,
                                quote_currency_name=name,
                                exchange_rate=exchange_rate.replace(',', '.'),
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
