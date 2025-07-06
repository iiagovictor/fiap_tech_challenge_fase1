from fastapi import APIRouter, HTTPException, Query
from app.api.v1.endpoint_categoria import (
    dados_csv,
)  # seu DataFrame com colunas 'title' e 'category'

router = APIRouter()


@router.get("/api/v1/books/search")
# /api/v1/books/search?title=Alice
# /api/v1/books/search?title=Alice&category=Fantasy
# /api/v1/books/search?category=Fantasy
async def search_books(
    title_param: str | None = Query(
        default=None, alias="title", description="Título ou parte do título do livro"
    ),
    category_param: str | None = Query(
        default=None, alias="category", description="Categoria do livro"
    ),
):
    if not title_param and not category_param:
        raise HTTPException(
            status_code=400,
            detail="Você deve informar ao menos o título ou a categoria.",
        )

    df_filtrado = dados_csv

    if title_param:
        df_filtrado = df_filtrado[
            df_filtrado["title"].str.contains(title_param, case=False, na=False)
        ]

    if category_param:
        df_filtrado = df_filtrado[
            df_filtrado["category"].str.lower() == category_param.lower()
        ]

    if df_filtrado.empty:
        if title_param and category_param:
            raise HTTPException(
                status_code=404,
                detail="Livro não encontrado ou não pertence à categoria informada.",
            )
        elif title_param:
            raise HTTPException(status_code=404, detail="Livro não encontrado.")
        else:
            raise HTTPException(
                status_code=404,
                detail="Nenhum livro encontrado para a categoria informada.",
            )

    return {
        "Success": True,
        "Message": "Resultado encontrado com sucesso.",
        "Data": df_filtrado.to_dict(orient="records"),
    }
