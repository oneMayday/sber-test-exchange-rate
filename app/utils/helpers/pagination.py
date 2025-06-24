from pydantic import (
    BaseModel,
    Field,
)


class PaginationInput(BaseModel):
    """Класс пагинации, инпут."""
    page: int = Field(1, ge=1, description="Page number (starting from 1)")
    per_page: int = Field(10, ge=1, le=100, description="Number of elements per page (from 1 to 100)")


class PaginationResponse(PaginationInput):
    """Класс пагинации, ответ."""
    total: int = Field(description="Total number of items")
