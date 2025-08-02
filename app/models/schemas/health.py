from typing import List
from pydantic import BaseModel, Field
from app.models.schemas.books import (
    BookItem
)


class HealthData(BaseModel):
    recordCount: int = Field(..., example=100)
    sampleData: List[BookItem] = Field(default_factory=list)


class HealthResponse(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Health check realizado com sucesso.")
    data: HealthData
