from fastapi import APIRouter, HTTPException
from typing import Optional
from app.api.root import dados_csv
from app.utils import helpers

router = APIRouter()


@router.get("/api/v1/books/price-range")
async def get_min_max_price(min: Optional[float] = None,
                            max: Optional[float] = None
                            ):
    """
    ### 📂 Pesquisa por livros em uma faixa de preço
    Este endpoint retorna uma lista de todos os livros que estão dentro de uma faixa de preço
    minimo e maximo.
    #### Como usar:
    - Faça uma requisição GET para `/api/v1/books/price-range`.
    - Inserir os argumentos min e max, juntamente com o valor desejado para cada
    parâmetro, como por exemplo: 'price-range?min=22.00&max=28.00', desa forma buscando todos
    os livros que tem um range de preço entre 22.00 e 28.00.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    """  # noqa: E501
    try:
        if len(dados_csv) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        resultado_filtragem_precos = helpers.get_price_range(
            dados_csv, "price_including_tax", min, max
            )
        return {
                "Success": True,
                "Message": "Valores retornados com sucesso",
                "Data": {
                    "books": resultado_filtragem_precos.to_dict(
                        orient="records"
                        )
                }
        }
    except HTTPException as http_error:
        raise http_error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno : {error}"
        )
