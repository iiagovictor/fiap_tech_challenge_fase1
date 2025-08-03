from fastapi import APIRouter, HTTPException, Query, Request, Depends
from app.api.v1.auth import get_current_user
from app.utils.helpers import get_unique_items
from app.api.root import dados_csv
from app.models.schemas.books import (
    BookDetailResponse,
    BooksSearchResponse,
    BooksListResponse
)
from app.utils.app_logger import AppLogger
from app.models.logger import LoggerModel
import time

router = APIRouter(tags=["Core"])


@router.get("/api/v1/books", response_model=BooksListResponse)
async def get_books(request: Request, user=Depends(get_current_user)):
    """### 📚 Listar Livros
    Este endpoint retorna uma lista de todos os livros disponíveis na coleção.
    Esta lista é ordenada alfabeticamente e contém apenas os títulos dos livros.

    #### Como usar:
    -   Faça uma requisição GET para `/api/v1/books`.
    -   A resposta será uma lista de títulos de livros ordenados alfabeticamente.
    -   É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    start_time = time.time()
    try:
        books = get_unique_items(dados_csv, "title")
        books = sorted(books, key=lambda x: x.lower())
        if len(books) == 0:
            latency = time.time() - start_time
            AppLogger().set_log_message(
                AppLogger().create_logger("books"),
                LoggerModel(
                    status_code=400,
                    endpoint="/api/v1/books",
                    message="Arquivo CSV não está populado.",
                    type="warning",
                    method=request.method,
                    latency=latency
                )
            )
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("books"),
            LoggerModel(
                status_code=200,
                endpoint="/api/v1/books",
                message="Livros retornados com sucesso.",
                type="info",
                method=request.method,
                latency=latency
            )
        )
        return {
            "success": True,
            "message": "Livros retornadas com sucesso.",
            "data": {
                "books": books
            }
        }
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("books"),
            LoggerModel(
                status_code=500,
                endpoint="/api/v1/books",
                message=f"Erro interno: {error}",
                type="error",
                method=request.method,
                latency=latency
            )
        )
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno : {error}"
        )


@router.get("/api/v1/books/search", response_model=BooksSearchResponse)
async def get_search_books(
    title_param: str | None = Query(
        default=None, alias="title",
        description="Título ou parte do título do livro"
    ),
    category_param: str | None = Query(
        default=None, alias="category", description="Categoria do livro"
    ),
    request: Request = None,
    user=Depends(get_current_user)
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
    -   Se o query parameter for inválido, a API retornará um erro 400 com uma mensagem detalhando os parâmetros permitidos.
    -   É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    start_time = time.time()
    allowed_params = {"title", "category"}
    query_params = set(request.query_params.keys())
    extras = query_params - allowed_params
    if extras:
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("books"),
            LoggerModel(
                status_code=400,
                endpoint="/api/v1/books/search",
                message=f"Parâmetros não permitidos: {', '.join(extras)}.",
                type="warning",
                method=request.method,
                latency=latency
            )
        )
        raise HTTPException(
            status_code=400,
            detail=(
                f"Parâmetros não permitidos: '{', '.join(extras)}'. "
                "Somente são aceitos: title, category."
            )
        )
    if not title_param and not category_param:
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("books"),
            LoggerModel(
                status_code=400,
                endpoint="/api/v1/books/search",
                message="Nenhum parâmetro de busca fornecido.",
                type="warning",
                method=request.method,
                latency=latency
            )
        )
        raise HTTPException(
            status_code=400,
            detail="Pelo menos um parâmetro de busca deve ser fornecido (title ou category)."  # noqa: E501
        )
    if category_param:
        categorias_validas = get_unique_items(dados_csv, "category")
        if category_param not in categorias_validas:
            latency = time.time() - start_time
            AppLogger().set_log_message(
                AppLogger().create_logger("books"),
                LoggerModel(
                    status_code=400,
                    endpoint="/api/v1/books/search",
                    message=f"Categoria '{category_param}' não é permitida.",
                    type="warning",
                    method=request.method,
                    latency=latency
                )
            )
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Categoria '{category_param}' não é permitida. "
                    f"Categorias válidas: {categorias_validas}"
                )
            )
    df_filter = dados_csv
    if title_param:
        df_filter = df_filter[
            df_filter["title"].str.contains(
                title_param,
                case=False,
                na=False
            )
        ]
    if category_param:
        df_filter = df_filter[
            df_filter["category"].str.lower() == category_param.lower()
        ]
    if df_filter.empty:
        latency = time.time() - start_time
        if title_param and category_param:
            AppLogger().set_log_message(
                AppLogger().create_logger("books"),
                LoggerModel(
                    status_code=404,
                    endpoint="/api/v1/books/search",
                    message="Livro não encontrado ou não pertence à categoria informada.",  # noqa: E501
                    type="warning",
                    method=request.method,
                    latency=latency
                )
            )
            raise HTTPException(
                status_code=404,
                detail=(
                    "Livro não encontrado ou não pertence à categoria informada."  # noqa: E501
                )
            )
        elif title_param:
            AppLogger().set_log_message(
                AppLogger().create_logger("books"),
                LoggerModel(
                    status_code=404,
                    endpoint="/api/v1/books/search",
                    message="Livro não encontrado.",
                    type="warning",
                    method=request.method,
                    latency=latency
                )
            )
            raise HTTPException(
                status_code=404,
                detail="Livro não encontrado."
            )
        else:
            AppLogger().set_log_message(
                AppLogger().create_logger("books"),
                LoggerModel(
                    status_code=404,
                    endpoint="/api/v1/books/search",
                    message="Nenhum livro encontrado para a categoria informada.",  # noqa: E501
                    type="warning",
                    method=request.method,
                    latency=latency
                )
            )
            raise HTTPException(
                status_code=404,
                detail="Nenhum livro encontrado para a categoria informada."
            )
    latency = time.time() - start_time
    AppLogger().set_log_message(
        AppLogger().create_logger("books"),
        LoggerModel(
            status_code=200,
            endpoint="/api/v1/books/search",
            message="Resultado encontrado com sucesso.",
            type="info",
            method=request.method,
            latency=latency
        )
    )
    return {
        "success": True,
        "message": "Resultado encontrado com sucesso.",
        "data": df_filter.to_dict(orient="records"),
    }


@router.get("/api/v1/books/top-rated")
async def get_top_rated_books(request: Request, user=Depends(get_current_user)):  # noqa: E501
    """### 🌟 Livros Mais Bem Avaliados
    Este endpoint retorna os livros mais bem avaliados, ou seja, aqueles que possuem a maior
    nota de avaliação (review_rating) igual a 5.

    #### Como usar:
    - Faça uma requisição GET para `/api/v1/books/top-rated`.
    - A resposta incluirá um dicionário com os títulos dos livros e suas respectivas avaliações
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    start_time = time.time()
    try:
        if len(dados_csv) == 0:
            latency = time.time() - start_time
            AppLogger().set_log_message(
                AppLogger().create_logger("books"),
                LoggerModel(
                    status_code=400,
                    endpoint="/api/v1/books/top-rated",
                    message="Arquivo CSV não está populado.",
                    type="warning",
                    method=request.method,
                    latency=latency
                )
            )
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        top_books = dados_csv[['title', 'review_rating']].query(
            "review_rating == 5")
        top_books = top_books.set_index('title')['review_rating'].to_dict()
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("books"),
            LoggerModel(
                status_code=200,
                endpoint="/api/v1/books/top-rated",
                message="Livros mais bem avaliados retornados com sucesso.",
                type="info",
                method=request.method,
                latency=latency
            )
        )
        return {
                "success": True,
                "Messamessagege": "Valores retornados com sucesso",
                "data": {
                    "Top rated books": top_books
                }
        }
    except Exception as error:
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("books"),
            LoggerModel(
                status_code=500,
                endpoint="/api/v1/books/top-rated",
                message=f"Erro interno: {error}",
                type="error",
                method=request.method,
                latency=latency
            )
        )
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno : {error}"
        )


@router.get("/api/v1/books/{book_id}", response_model=BookDetailResponse)
async def get_book_id(request: Request, book_id: int, user=Depends(get_current_user)):  # noqa: E501
    """### 📖 Detalhes do Livro por ID
    Este endpoint retorna os detalhes de um livro específico com base no seu ID.

    #### Como usar:
    -   Faça uma requisição GET para `/api/v1/books/{book_id}`, substituindo `{book_id}` pelo ID do livro desejado.
    -   A resposta incluirá um dicionário com os detalhes do livro, incluindo título, descrição, categoria, preço e outros atributos.
    -   Se o ID do livro não for encontrado, um erro 404 será retornado.
    -   É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    start_time = time.time()
    if 0 < book_id <= len(dados_csv):
        resultado = dados_csv[dados_csv["book_id"] == book_id]
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("books"),
            LoggerModel(
                status_code=200,
                endpoint="/api/v1/books/{book_id}",
                message=f"Livro encontrado com sucesso. ID: {book_id}",
                type="info",
                method=request.method,
                latency=latency
            )
        )
        return {
            "success": True,
            "message": "Livro encontrado com sucesso.",
            "data": {
                "book": resultado.to_dict(orient="records")[0]
            }
        }
    else:
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("books"),
            LoggerModel(
                status_code=404,
                endpoint="/api/v1/books/{book_id}",
                message=f"Livro não encontrado. ID: {book_id}",
                type="warning",
                method=request.method,
                latency=latency
            )
        )
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado."
        )
