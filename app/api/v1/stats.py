from fastapi import APIRouter, HTTPException, Depends, Request
from app.api.v1.auth import get_current_user
from app.api.root import dados_csv
from app.utils import helpers
from app.models.schemas.stats import (
    StatsOverviewResponse
)
from app.utils.app_logger import AppLogger
from app.models.logger import LoggerModel
import time

router = APIRouter(tags=["Stats"])


@router.get('/api/v1/stats/overview', response_model=StatsOverviewResponse)
async def get_overview_data(request: Request, user=Depends(get_current_user)):
    """### 📊 Visão Geral dos Dados
    Este endpoint fornece uma visão geral dos dados disponíveis na coleção de livros.
    Ele retorna o total de registros, a média de preços e a distribuição de avaliações.

    #### Como usar:
    - Faça uma requisição GET para `/api/v1/stats/overview`.
    - A resposta incluirá o número total de registros, a média de preços e a distribuição de avaliações.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    start_time = time.time()
    try:
        if len(dados_csv) == 0:
            latency = time.time() - start_time
            AppLogger().set_log_message(
                AppLogger().create_logger("stats"),
                LoggerModel(
                    status_code=400,
                    endpoint="/api/v1/stats/overview",
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
            AppLogger().create_logger("stats"),
            LoggerModel(
                status_code=200,
                endpoint="/api/v1/stats/overview",
                message="Overview sobre os dados retornado com sucesso.",
                type="info",
                method=request.method,
                latency=latency
            )
        )
        return {
            "success": True,
            "message": "Overview sobre os dados.",
            "data": {
                "total": len(dados_csv),
                "average": round(dados_csv['price_including_tax'].mean(), 2),
                "ratingsDistribution": {
                    "ratingOne": helpers.get_rating(
                        dados_csv, 'review_rating', 1, 0
                    ),
                    "ratingTwo": helpers.get_rating(
                        dados_csv, 'review_rating', 2, 0
                    ),
                    "ratingThree": helpers.get_rating(
                        dados_csv, 'review_rating', 3, 0
                    ),
                    "ratingFour": helpers.get_rating(
                        dados_csv, 'review_rating', 4, 0
                    ),
                    "ratingFive": helpers.get_rating(
                        dados_csv, 'review_rating', 5, 0
                    ),
                }
            }
        }
    except Exception as error:
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("stats"),
            LoggerModel(
                status_code=500,
                endpoint="/api/v1/stats/overview",
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


@router.get("/api/v1/stats/categories")
async def get_stats_categories(request: Request, user=Depends(get_current_user)):  # noqa: E501
    """### 📊 Estatísticas por Categoria
    Este endpoint retorna o número de livros por categoria e a média de preços por categoria.

    #### Como usar:
    - Faça uma requisição GET para `/api/v1/stats/categories`.
    - A resposta incluirá o número de livros por categoria e a média de preços por categoria.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    start_time = time.time()
    try:
        if len(dados_csv) == 0:
            latency = time.time() - start_time
            AppLogger().set_log_message(
                AppLogger().create_logger("stats"),
                LoggerModel(
                    status_code=400,
                    endpoint="/api/v1/stats/categories",
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
        number_books = dados_csv['category'].value_counts().to_dict()
        average_price = dados_csv.groupby(
            'category')['price_including_tax'].mean().round(2)
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("stats"),
            LoggerModel(
                status_code=200,
                endpoint="/api/v1/stats/categories",
                message="Valores de categorias retornados com sucesso.",
                type="info",
                method=request.method,
                latency=latency
            )
        )
        return {
                "success": True,
                "message": "Valores retornados com sucesso",
                "data": {
                    "numberBooks": number_books,
                    "averagePrice": average_price
                }
        }
    except Exception as error:
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("stats"),
            LoggerModel(
                status_code=500,
                endpoint="/api/v1/stats/categories",
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
