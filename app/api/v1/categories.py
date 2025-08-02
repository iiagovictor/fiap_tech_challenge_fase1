from fastapi import APIRouter, HTTPException, Depends
from app.api.v1.auth import get_current_user
from app.utils.helpers import get_unique_items
from app.api.root import dados_csv
from app.models.schemas.categories import (
    CategoriesResponse
)

router = APIRouter(tags=["Core"])


@router.get("/api/v1/categories", response_model=CategoriesResponse)
async def get_categories(user=Depends(get_current_user)):
    """
    ### 📂 Listar Categorias
    Este endpoint retorna uma lista de todas as categorias disponíveis na coleção de livros.
    As categorias são ordenadas alfabeticamente e não contêm duplicatas.
    #### Como usar:
    - Faça uma requisição GET para `/api/v1/categories`.
    - A resposta incluirá uma lista de categorias únicas, ordenadas alfabeticamente.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    try:
        df_filter = get_unique_items(dados_csv, "category")
        df_filter = sorted(df_filter, key=lambda x: x.lower())
        if len(df_filter) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        return {
            "success": True,
            "message": "Categorias retornadas com sucesso.",
            "data": {
                "total": len(df_filter),
                "categories": df_filter
            }
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno : {error}"
        )
