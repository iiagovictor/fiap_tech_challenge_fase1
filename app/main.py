from fastapi import FastAPI
from app.api.v1 import endpoint_categoria, endpoint_health, endpoint_retorna_books_por_id

app = FastAPI(
    title="API Categorias",
    version="1.0.0",
    description="Endpoint para verificação das categorias dos livros."
)

app.include_router(endpoint_categoria.router)
app.include_router(endpoint_retorna_books_por_id.router)
app.include_router(endpoint_health.router)

