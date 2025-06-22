from fastapi import FastAPI
from app.api.v1 import endpoint_categoria
from fiap_tech_challenge_fase1.app.utils.helpers import get_csv_data

app = FastAPI(
    title="API Categorias",
    version="1.0.0",
    description="Endpoint para verificação das categorias dos livros."
)


dados_csv = get_csv_data(rf'C:\Users\Victor\Desktop\CONEXAO_REPO_fiap_tech_challenge_fase1\fiap_tech_challenge_fase1\data\books.csv')

print(dados_csv)

app.include_router(endpoint_categoria.router, prefix="")
app.include_router(endpoint_categoria.router, prefix="/api/v1/categories")
