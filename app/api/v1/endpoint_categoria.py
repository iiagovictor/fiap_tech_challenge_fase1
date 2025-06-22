from fastapi import APIRouter
from fiap_tech_challenge_fase1.app.utils.helpers import get_csv_data

router = APIRouter()

dados_csv = get_csv_data(rf'C:\Users\Victor\Desktop\CONEXAO_REPO_fiap_tech_challenge_fase1\fiap_tech_challenge_fase1\data\books.csv')

print(dados_csv)

@router.get("/")
async def get_categories():
    return  "Somente para evitar erros"


@router.get("/api/v1/categories")
async def get_categories():
    return  "Teste"