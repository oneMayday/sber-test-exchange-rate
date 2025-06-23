from abc import ABC, abstractmethod

from .base_schemas import (
    GetExchangeRateLitProviderResponse,
    GetExchangeRateProviderRequestParams,
)


class FinancialDataBaseProvider(ABC):
    """Базовый класс поставщика финансовых данных."""
    provider_name = ''
    provider_url = ''

    @abstractmethod
    async def get_currencies_exchange_rates(
        self,
        request_params: GetExchangeRateProviderRequestParams
    ) -> GetExchangeRateLitProviderResponse:
        """Получение курсов обмена валют."""
        pass
