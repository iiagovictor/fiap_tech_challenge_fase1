from fastapi import FastAPI
from app.api.v1 import endpoint_categoria
from app.utils.helpers import get_csv_data
from pathlib import Path

app = FastAPI(
    title="API Categorias",
    version="1.0.0",
    description="Endpoint para verificação das categorias dos livros."
)

endpoint_categoria.dados_csv = get_csv_data(
    rf'data\books.csv'
)

app.include_router(endpoint_categoria.router)
