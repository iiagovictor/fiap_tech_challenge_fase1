from fastapi import APIRouter, HTTPException
from app.api.v1.endpoint_categoria import dados_csv

router = APIRouter()

@router.get("/api/v1/books/{book_id}")
async def get_book_by_id(book_id: int):
    if 0 < book_id <= len(dados_csv):
        resultado = dados_csv[dados_csv["book_id"] == book_id]
        return {
            "Success": True,
            "Message": "Categorias retornadas com sucesso.",
            "Data":{
                "Book":resultado.to_dict()
            }
        }
    else:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado."
        )
