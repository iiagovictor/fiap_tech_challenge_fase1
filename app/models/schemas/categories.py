from typing import List
from pydantic import BaseModel, Field


class CategoriesData(BaseModel):
    total: int = Field(..., example=2)
    categories: List[str] = Field(..., example=["Poetry", "Fiction"])


class CategoriesResponse(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Categorias retornadas com sucesso.")
    data: CategoriesData
