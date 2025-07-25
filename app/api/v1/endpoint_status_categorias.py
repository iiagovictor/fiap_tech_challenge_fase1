from fastapi import APIRouter, HTTPException
from app.api.v1.endpoint_categoria import dados_csv

router = APIRouter()


@router.get("/api/v1/stats/categories")
async def get_stats_categories():
    try:
        if len(dados_csv) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        number_books = dados_csv['category'].value_counts().to_dict()
        average_price = dados_csv.groupby(
            'category')['price_including_tax'].mean().round(2)
        return {
                "Success": True,
                "Message": "Valores retornados com sucesso",
                "Data": {
                    "Number of books": number_books,
                    "Average price": average_price
                }
        }
    except HTTPException as http_error:
        raise http_error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno : {error}"
        )
