from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.utils.helpers import get_csv_data
from app.utils.app_logger import AppLogger
from app.models.logger import LoggerModel
import os
import time

router = APIRouter(tags=["Core"])

dados_csv = get_csv_data(os.path.join(os.path.dirname(__file__), "../data/books.csv"))  # noqa: E501


@router.get("/")
async def get_home(request: Request):
    """### 🏠 Página Inicial
    Este é o ponto de entrada da API. Você pode acessar a documentação da API em `/docs`.
    #### Como usar:
    - Acesse a raiz da API em `/`.
    - Você será redirecionado para a documentação interativa da API.
    """  # noqa: E501
    start_time = time.time()
    latency = time.time() - start_time
    AppLogger().set_log_message(
        AppLogger().create_logger("root"),
        LoggerModel(
            status_code=200,
            endpoint="/",
            message="Acesso à página inicial e redirecionamento para /docs.",
            type="info",
            method=request.method,
            latency=latency
        )
    )
    return RedirectResponse(url="/docs")
