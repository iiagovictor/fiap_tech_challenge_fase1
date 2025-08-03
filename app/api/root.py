from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.utils.helpers import get_csv_data
import os

router = APIRouter(tags=["Core"])

dados_csv = get_csv_data(os.path.join(os.path.dirname(__file__), "../data/books.csv"))  # noqa: E501


@router.get("/")
async def get_home():
    """### 🏠 Página Inicial
    Este é o ponto de entrada da API. Você pode acessar a documentação da API em `/docs`.
    #### Como usar:
    - Acesse a raiz da API em `/`.
    - Você será redirecionado para a documentação interativa da API.
    """  # noqa: E501
    return RedirectResponse(url="/docs")
