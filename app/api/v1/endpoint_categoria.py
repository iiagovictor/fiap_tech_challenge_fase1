from fastapi import APIRouter, HTTPException
from app.utils.helpers import get_csv_data, get_only_categories

router = APIRouter()

dados_csv = get_csv_data(rf'data\books.csv')
#dados_csv = get_csv_data(rf'data\books_empty.csv')
#dados_csv = get_csv_data(rf'data\books_without_data.csv')

@router.get("/")
async def home():
    return  "Somente para evitar erros"


@router.get("/api/v1/categories")
async def get_categories():
    try:
        dados_filtrados = get_only_categories(dados_csv)
        if len(dados_filtrados) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        return {
            "Success": True,
            "Message": "Categorias retornadas com sucesso.",
            "Data":{
                "Categories":dados_filtrados
            }
        }
    except HTTPException as http_error:
        raise http_error 

    except Exception as error:
        raise   HTTPException(
            status_code=500,
            detail=f"Erro interno : {error}"
        )
