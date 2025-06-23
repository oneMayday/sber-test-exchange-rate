from sqlalchemy import select, delete, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import (
    Currency,
    ExchangeRate
)
from ..schemas import (
    ExchangeRateGetAllDataResponse,
    CurrencyExchangeRate
)


class ExchangeRateModelService:
    """Сервис взаимодействия БД с моделью Currency"""

    model = ExchangeRate

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self):
        stmt = select(self.model)
        result: Result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all_data(self, page: int, per_page: int) -> ExchangeRateGetAllDataResponse:
        count = await self.session.scalar(select(func.count(self.model.id)))
        skip = (page - 1) * 10
        total = count / per_page if count % per_page == 0 else count // per_page + 1

        stmt = (
            select(
                ExchangeRate.id,
                Currency.code,
                ExchangeRate.rate,
                ExchangeRate.date,
            )
            .join(Currency, ExchangeRate.quote_currency)
        ).offset(skip).limit(per_page)

        result: Result = await self.session.execute(stmt)

        items = [
            CurrencyExchangeRate(
                id=row.id, code=row.code, rate=row.rate, date=row.date
            )
            for row in result
        ]

        return ExchangeRateGetAllDataResponse(
            page=page,
            per_page=per_page,
            total=total,
            items=items,
        )

    async def save_bulk(self, exchange_rates: list[ExchangeRate]):
        self.session.add_all(exchange_rates)
        await self.session.commit()

    async def delete_by_code(self, code: str):
        stmt = delete(
            ExchangeRate
        ).where(
            ExchangeRate.id.in_(
                select(
                    ExchangeRate.id
                ).join(
                    ExchangeRate.quote_currency
                ).filter(
                    Currency.code == code.upper()
                )
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()
