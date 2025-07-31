from fastapi import APIRouter, HTTPException, Query
from app.api.v1.endpoint_categoria import (
    dados_csv,
)

router = APIRouter(tags=["Core"])


@router.get("/api/v1/books/search")
async def search_books(
    title_param: str | None = Query(
        default=None, alias="title",
        description="Título ou parte do título do livro"),
    category_param: str | None = Query(
        default=None, alias="category", description="Categoria do livro"
    ),
):
    """
    ### 🔍 Pesquisar Livros por Título e/ou Categoria

    Este endpoint permite que os usuários busquem livros na coleção utilizando um ou ambos os critérios: **título** e **categoria**.

    #### Como usar:

    Para realizar uma busca, utilize os parâmetros de query `title` e/ou `category`.

    -   **Busca por Título:**
        -   `GET /api/v1/books/search?title=NomeDoLivro`
        -   *Exemplo:* `/api/v1/books/search?title=Alice`

    -   **Busca por Título e Categoria:**
        -   `GET /api/v1/books/search?title=NomeDoLivro&category=NomeDaCategoria`
        -   *Exemplo:* `/api/v1/books/search?title=Alice&category=Fantasy`

    -   **Busca por Categoria:**
        -   `GET /api/v1/books/search?category=NomeDaCategoria`
        -   *Exemplo:* `/api/v1/books/search?category=Fantasy`

    **Observações Importantes:**
    -   A busca por **título** é **case-insensitive** (não diferencia maiúsculas de minúsculas).
    -   A busca por **categoria** também é **case-insensitive**, pois o valor fornecido é convertido para minúsculas antes da comparação.
    -   Se nenhum critério (`title` ou `category`) for fornecido, a API retornará um erro 400.
    -   Se nenhum livro for encontrado com os critérios fornecidos, um erro 404 será retornado.
    """
    if not title_param and not category_param:
        raise HTTPException(
            status_code=400,
            detail="Você deve informar ao menos o título ou a categoria.",
        )

    df_filtrado = dados_csv

    if title_param:
        df_filtrado = df_filtrado[
            df_filtrado["title"].str.contains(
                title_param,
                case=False,
                na=False
            )
        ]

    if category_param:
        df_filtrado = df_filtrado[
            df_filtrado["category"].str.lower() == category_param.lower()
        ]

    if df_filtrado.empty:
        if title_param and category_param:
            raise HTTPException(
                status_code=404,
                detail="Livro não encontrado"
                "ou não pertence à categoria informada.",
            )
        elif title_param:
            raise HTTPException(status_code=404,
                                detail="Livro não encontrado.")
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
