from fastapi import APIRouter
from app.utils.helpers import get_csv_data
from typing import List, Dict

router = APIRouter()
dados_csv = []

@router.get("/")
async def home():
    return  "Somente para evitar erros"


@router.get("/api/v1/categories")
async def get_categories():
    return  dados_csv