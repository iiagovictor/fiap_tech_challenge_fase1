from fastapi import APIRouter, HTTPException, Depends, Request
from app.api.v1.auth import get_current_user
from typing import Optional
from app.api.root import dados_csv
from app.utils import helpers
from app.utils.app_logger import AppLogger
from app.models.logger import LoggerModel
import time


router = APIRouter(tags=["Insights"])


@router.get("/api/v1/books/price-range")
async def get_min_max_price(request: Request, min: Optional[float] = None,
                            max: Optional[float] = None,
                            user=Depends(get_current_user)
                            ):
    """
    ### 📂 Pesquisa por livros em uma faixa de preço
    Este endpoint retorna uma lista de todos os livros que estão dentro de uma faixa de preço
    minimo e maximo.
    #### Como usar:
    - Faça uma requisição GET para `/api/v1/books/price-range`.
    - Inserir os argumentos min e max, juntamente com o valor desejado para cada
    parâmetro, como por exemplo: 'price-range?min=22.00&max=28.00', desa forma buscando todos
    os livros que tem um range de preço entre 22.00 e 28.00.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    start_time = time.time()
    try:
        if len(dados_csv) == 0:
            latency = time.time() - start_time
            AppLogger().set_log_message(
                AppLogger().create_logger("price-range"),
                LoggerModel(
                    status_code=400,
                    endpoint="/api/v1/books/price-range",
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
        resultado_filtragem_precos = helpers.get_price_range(
            dados_csv, "price_including_tax", min, max
            )
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("price-range"),
            LoggerModel(
                status_code=200,
                endpoint="/api/v1/books/price-range",
                message="Valores de livros por faixa de preço retornados com sucesso.",  # noqa: E501
                type="info",
                method=request.method,
                latency=latency
            )
        )
        return {
                "Success": True,
                "Message": "Valores retornados com sucesso",
                "Data": {
                    "books": resultado_filtragem_precos.to_dict(
                        orient="records"
                        )
                }
        }
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("price-range"),
            LoggerModel(
                status_code=500,
                endpoint="/api/v1/books/price-range",
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
