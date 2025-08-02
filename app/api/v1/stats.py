from fastapi import APIRouter, HTTPException, Depends
from app.api.v1.auth import get_current_user
from app.api.root import dados_csv
from app.utils import helpers
from app.models.schemas.stats import (
    StatsOverviewResponse
)

router = APIRouter(tags=["Insights"])


@router.get('/api/v1/stats/overview', response_model=StatsOverviewResponse)
async def get_overview_data(user=Depends(get_current_user)):
    """### 📊 Visão Geral dos Dados
    Este endpoint fornece uma visão geral dos dados disponíveis na coleção de livros.
    Ele retorna o total de registros, a média de preços e a distribuição de avaliações.

    #### Como usar:
    - Faça uma requisição GET para `/api/v1/stats/overview`.
    - A resposta incluirá o número total de registros, a média de preços e a distribuição de avaliações.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    try:
        if len(dados_csv) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
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
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno : {error}"
        )
