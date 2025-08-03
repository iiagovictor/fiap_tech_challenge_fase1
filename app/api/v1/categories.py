from fastapi import APIRouter, HTTPException, Depends, Request
from app.api.v1.auth import get_current_user
from app.utils.helpers import get_unique_items
from app.api.root import dados_csv
from app.models.schemas.categories import (
    CategoriesResponse
)
from app.utils.app_logger import AppLogger
from app.models.logger import LoggerModel
import time

router = APIRouter(tags=["Core"])


@router.get("/api/v1/categories", response_model=CategoriesResponse)
async def get_categories(request: Request, user=Depends(get_current_user)):
    """
    ### 📂 Listar Categorias
    Este endpoint retorna uma lista de todas as categorias disponíveis na coleção de livros.
    As categorias são ordenadas alfabeticamente e não contêm duplicatas.
    #### Como usar:
    - Faça uma requisição GET para `/api/v1/categories`.
    - A resposta incluirá uma lista de categorias únicas, ordenadas alfabeticamente.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    start_time = time.time()
    try:
        df_filter = get_unique_items(dados_csv, "category")
        df_filter = sorted(df_filter, key=lambda x: x.lower())
        if len(df_filter) == 0:
            latency = time.time() - start_time
            AppLogger().set_log_message(
                AppLogger().create_logger("categories"),
                LoggerModel(
                    status_code=400,
                    endpoint="/api/v1/categories",
                    message="Arquivo CSV não está populado.",
                    type="warning",
                    method=request.method,
                    latency=latency
                )
            )
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("categories"),
            LoggerModel(
                status_code=200,
                endpoint="/api/v1/categories",
                message="Categorias retornadas com sucesso.",
                type="info",
                method=request.method,
                latency=latency
            )
        )
        return {
            "success": True,
            "message": "Categorias retornadas com sucesso.",
            "data": {
                "total": len(df_filter),
                "categories": df_filter
            }
        }
    except Exception as error:
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("categories"),
            LoggerModel(
                status_code=500,
                endpoint="/api/v1/categories",
                message=f"Erro interno: {error}",
                type="error",
                method=request.method,
                latency=latency
            )
        )
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno : {error}"
        )
