from fastapi import FastAPI
from app.api.v1 import endpoint_categoria

app = FastAPI(
    title="API Categorias",
    version="1.0.0",
    description="Endpoint para verificação das categorias dos livros."
)

app.include_router(endpoint_categoria.router, prefix="")
app.include_router(endpoint_categoria.router, prefix="/api/v1/categories")
