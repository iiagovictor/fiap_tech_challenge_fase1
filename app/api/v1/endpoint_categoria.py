from fastapi import APIRouter
from app.utils.helpers import get_csv_data, get_only_categories

router = APIRouter()

#dados_csv = get_csv_data(rf'data\books.csv')
#dados_csv = get_csv_data(rf'data\books_empty.csv')
dados_csv = get_csv_data(rf'data\books_without_data.csv')

@router.get("/")
async def home():
    return  "Somente para evitar erros"

#Padronizar o retorno para aquilo que o Iago falou
@router.get("/api/v1/categories")
async def get_categories():
    dados_filtrados = get_only_categories(dados_csv)
    return  dados_filtrados