from pydantic import (
    BaseModel,
    Field,
)


class PaginationInput(BaseModel):
    """Класс пагинации, инпут."""
    page: int = Field(1, ge=1, description="Номер страницы (начиная с 1)")
    per_page: int = Field(10, ge=1, le=100, description="Количество элементов на странице (от 1 до 100)")


class PaginationResponse(PaginationInput):
    """Класс пагинации, ответ."""
    total: int = Field(description="Общее количество элементов")
