from fastapi import FastAPI
from app.api.v1 import (
    endpoint_categoria,
    endpoint_health,
    endpoint_retorna_books_por_id,
    endpoint_overview,
    endpoint_lista_livros_disponiveis,
)


app = FastAPI(
    title="Our FastAPI API",
    version="1.0.0",
    description="API de Consultas de Livros com FASTAPI"
)

app.include_router(endpoint_categoria.router)
app.include_router(endpoint_retorna_books_por_id.router)
app.include_router(endpoint_health.router)
app.include_router(endpoint_overview.router)
app.include_router(endpoint_lista_livros_disponiveis.router)
