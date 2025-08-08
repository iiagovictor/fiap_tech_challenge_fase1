from fastapi import APIRouter, Depends, HTTPException
from app.services.service import get_recommendations_from_title
from app.api.v1.auth import get_current_user
from app.models.schemas.recommender import (
    RecomendarRequest,
    RecomendacoesResponse
)


router = APIRouter(tags=["ML"])


@router.post("/api/v1/ml/predictions", response_model=RecomendacoesResponse)
async def recomendar_livros(item: RecomendarRequest,
                            user=Depends(get_current_user)
                            ):
    """
    ### Descubra sua Próxima Grande Leitura! 🚀
    Use este endpoint para receber recomendações de livros personalizadas.
    Basta fornecer o título de um livro que você amou e deixe nossa inteligência artificial # noqa: E501
    fazer a mágica, encontrando obras similares que podem ser sua próxima obsessão.

    **Como funciona?**
    - **Entrada:** Um objeto JSON com o título do seu livro favorito.
    - **Processamento:** Nosso modelo de machine learning analisa o título e busca
    livros com características e temas semelhantes.
    - **Saída:** Uma lista de títulos recomendados, pronta para inspirar sua lista de leitura.

    **Exemplo de sucesso:**
    - Você envia "Night Sky with Exit Wounds".
    - Nós retornamos:
    `{"livro_base":"Night Sky with Exit Wounds",`
    `"recomendacoes":["Slow States of Collapse: Poems",
                    "Les Fleurs du Mal", "Booked", "salt.",
                    "Shakespeare's Sonnets", "I'll Give You the Sun",
                    "Tell the Wolves I'm Home", "Howl and Other Poems",
                    "Twenty Love Poems and a Song of Despair",
                    "A Light in the Attic"]}`

    **Status de Erro:**
    - `404 Not Found`: Título do livro não encontrado em nossa base de dados.
    - `500 Internal Server Error`: Ocorreu um problema inesperado no
        nosso sistema de recomendação.
    """
    try:
        titulo = item.titulo_livro.strip()
        recomendacoes = get_recommendations_from_title(title=titulo)
        return RecomendacoesResponse(
            livro_base=titulo,
            recomendacoes=recomendacoes
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreu um erro ao gerar as recomendações: {e}"
        )
