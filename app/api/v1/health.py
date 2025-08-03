from fastapi import APIRouter, HTTPException, Depends, Request
from app.api.v1.auth import get_current_user
from app.api.root import dados_csv
from app.models.schemas.health import (
    HealthResponse
)
from app.utils.app_logger import AppLogger
from app.models.logger import LoggerModel
import time

router = APIRouter(tags=["Core"])


@router.get("/api/v1/health", response_model=HealthResponse)
async def health(request: Request, user=Depends(get_current_user)):
    """### ✅ Endpoint para verificar a saúde da API.
    Retorna o número de registros no CSV e alguns dados de amostra.

    #### Como usar:
    - Faça uma requisição GET para `/api/v1/health`.
    - A resposta incluirá o número total de registros e alguns dados de amostra.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    start_time = time.time()
    try:
        if dados_csv.empty:
            latency = time.time() - start_time
            AppLogger().set_log_message(
                AppLogger().create_logger("health"),
                LoggerModel(
                    status_code=400,
                    endpoint="/api/v1/health",
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
            AppLogger().create_logger("health"),
            LoggerModel(
                status_code=200,
                endpoint="/api/v1/health",
                message="Health check realizado com sucesso.",
                type="info",
                method=request.method,
                latency=latency
            )
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
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("health"),
            LoggerModel(
                status_code=500,
                endpoint="/api/v1/health",
                message=f"Erro interno: {error}",
                type="error",
                method=request.method,
                latency=latency
            )
        )
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno {error}"
        )
