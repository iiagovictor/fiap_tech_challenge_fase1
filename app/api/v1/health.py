from fastapi import APIRouter, HTTPException, Depends
from app.api.v1.auth import get_current_user
from app.api.root import dados_csv
from app.models.schemas.health import (
    HealthResponse
)

router = APIRouter(tags=["Core"])


@router.get("/api/v1/health", response_model=HealthResponse)
async def health(user=Depends(get_current_user)):
    """### ✅ Endpoint para verificar a saúde da API.
    Retorna o número de registros no CSV e alguns dados de amostra.

    #### Como usar:
    - Faça uma requisição GET para `/api/v1/health`.
    - A resposta incluirá o número total de registros e alguns dados de amostra.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    try:
        if dados_csv.empty:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        return {
            "success": True,
            "message": "Health check realizado com sucesso.",
            "data": {
                "recordCount": len(dados_csv),
                "sampleData": dados_csv.head(5).to_dict(orient="records")
            }
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno {error}"
        )
