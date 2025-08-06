from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from app.services.service import get_recommendations_from_title
from app.models.schemas.recommender import RecomendarRequest, RecomendacoesResponse


router = APIRouter(tags=["ML"])


@router.post("/api/v1/ml/predictions", response_model=RecomendacoesResponse)
async def recomendar_livros(item: RecomendarRequest):
    """
    ### Endpoint de Recomendação de Livros
    Este endpoint recebe o título de um livro e retorna uma lista de recomendações.
    """
    try:
        titulo = item.titulo_livro.strip()
        
        recomendacoes = get_recommendations_from_title(title=titulo)
        
        return RecomendacoesResponse(livro_base=titulo, recomendacoes=recomendacoes)

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