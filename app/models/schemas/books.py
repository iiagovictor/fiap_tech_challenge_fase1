from typing import List
from pydantic import BaseModel, Field


class BooksListData(BaseModel):
    books: List[str] = Field(..., example=[
        "A Feast for Crows (A Song of Ice and Fire #4)",
        "Alice in Wonderland (Alice's Adventures in Wonderland #1)"
    ])


class BooksListResponse(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Livros retornadas com sucesso.")
    data: BooksListData


class BookItem(BaseModel):
    book_id: int
    title: str
    description: str
    review_rating: int
    category: str
    product_upc: str
    currency: str
    price_including_tax: float
    price_excluding_tax: float
    tax: float
    number_available: int
    created_at: str
    image_url: str
    url: str


class BooksSearchResponse(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Resultado encontrado com sucesso.")
    data: List[BookItem]


class BookDetailData(BaseModel):
    book: BookItem


class BookDetailResponse(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Livro encontrado com sucesso.")
    data: BookDetailData
