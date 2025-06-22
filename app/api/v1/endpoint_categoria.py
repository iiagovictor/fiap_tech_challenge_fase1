from fastapi import APIRouter
from app.utils.helpers import get_csv_data, get_only_categories

router = APIRouter()

dados_csv = get_csv_data(rf'data\books.csv')


@router.get("/")
async def home():
    return  "Somente para evitar erros"

@router.get("/api/v1/categories")
async def get_categories():
    dados_filtrados = get_only_categories(dados_csv)
    return  dados_filtrados