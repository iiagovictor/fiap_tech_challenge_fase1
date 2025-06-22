from fastapi import APIRouter
from app.api.v1.endpoint_categoria import dados_csv

router = APIRouter()

@router.get("/api/v1/health")
async def health():
    if dados_csv.empty:
        return{
            "Status da API": "Erro",
            "Msg": "Arquivo CSV não possui registros"
        }
    return {
        "Status da API": 200,
        "Quantidade de registros no CSV": len(dados_csv)
    }
