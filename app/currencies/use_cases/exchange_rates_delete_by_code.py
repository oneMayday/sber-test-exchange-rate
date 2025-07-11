from typing import NoReturn

from sqlalchemy.ext.asyncio import AsyncSession

from ..model_services import ExchangeRateModelService
from ..schemas import ExchangeRateDeleteByCodeResponse


class ExchangeRatesDeleteByCodeUseCase:
    """Удаление всех записей о курсах валют, по коду валюты."""
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.exchange_rate_model_service = ExchangeRateModelService(self.session)

    async def execute(self, currency_code: str) -> ExchangeRateDeleteByCodeResponse | NoReturn:
        await self.exchange_rate_model_service.delete_by_code(currency_code)
        return ExchangeRateDeleteByCodeResponse(message=f"All records for {currency_code.upper()} deleted successfully")
