from sqlalchemy.ext.asyncio import AsyncSession

from ..model_services import ExchangeRateModelService


class ExchangeRatesDeleteByCodeUseCase:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.exchange_rate_model_service = ExchangeRateModelService(self.session)

    async def execute(self, currency_code: str) -> list[str]:
        result = await self.exchange_rate_model_service.delete_by_code(currency_code)
        return result
