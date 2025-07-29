from fastapi import APIRouter, HTTPException
from app.api.v1.endpoint_categoria import dados_csv

router = APIRouter()


@router.get("/api/v1/books/top-rated")
async def get_top_rated_books():
    try:
        if len(dados_csv) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        top_books = dados_csv[['title', 'review_rating']].query(
            "review_rating == 5")
        top_books = top_books.set_index('title')['review_rating'].to_dict()

        return {
                "Success": True,
                "Message": "Valores retornados com sucesso",
                "Data": {
                    "Top rated books": top_books
                }
        }
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno : {error}"
        )
