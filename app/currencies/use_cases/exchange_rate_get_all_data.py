from datetime import datetime
from decimal import Decimal
from typing import NoReturn

from sqlalchemy.ext.asyncio import AsyncSession

from ..model_services import ExchangeRateModelService
from ..schemas import ExchangeRateGetAllDataResponse, CurrencyExchangeRate


class ExchangeRatesGetAllDataUseCase:
    """Получение всех данных о курсах валют, с пагинацией."""
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.exchange_rate_model_service = ExchangeRateModelService(self.session)

    async def execute(self, page: int, per_page: int) -> ExchangeRateGetAllDataResponse | NoReturn:
        return await self.exchange_rate_model_service.get_all_data(
            page=page,
            per_page=per_page
        )
