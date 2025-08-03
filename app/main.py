from fastapi import FastAPI
from app.api import root
from app.api.v1 import (
    books,
    categories,
    health,
    stats,
    users,
    auth
)

app = FastAPI(
    title="FIAP - Biblioteca Digital API",
    version="1.0.0",
    description="API para consulta, pesquisa e análise de livros da Biblioteca Digital FIAP. Permite acesso a informações detalhadas, categorias, estatísticas e health check dos dados."  # noqa: E501
)

app.include_router(root.router)
app.include_router(categories.router)
app.include_router(health.router)
app.include_router(stats.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(auth.router)
