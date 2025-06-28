from fastapi import APIRouter, HTTPException
from app.utils.helpers import get_csv_data, get_only_books

router = APIRouter()

dados_csv = get_csv_data(rf'data\books.csv')

@router.get("/api/v1/books:")

async def get_books():
    try:
        livros_filtrados = get_only_books(dados_csv)
        if len(livros_filtrados) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        return {
            "Success": True,
            "Message": "Livros retornadas com sucesso.",
            "Data":{
                "Livros":livros_filtrados
            }
        }
    except HTTPException as http_error:
        raise http_error 

    except Exception as error:
        raise   HTTPException(
            status_code=500,
            detail=f"Erro interno : {error}"
        )
