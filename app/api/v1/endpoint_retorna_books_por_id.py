from fastapi import APIRouter, HTTPException
from app.api.v1.endpoint_categoria import dados_csv
from app.models.logger import LoggerModel
from app.utils.app_logger import AppLogger

router = APIRouter()

log = AppLogger()
logger = log.create_logger(__name__)

@router.get("/api/v1/books/{book_id}")
async def get_book_by_id(book_id: int):
    endpoint = router.url_path_for("get_book_by_id")
    try:
        if 0 < book_id <= len(dados_csv):
            resultado = dados_csv[dados_csv["book_id"] == book_id]
            return {
                "Success": True,
                "Message": "Categorias retornadas com sucesso.",
                "Data": {
                    "Book": resultado.to_dict(orient="records")[0]
                }
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="Livro não encontrado."
            )
    except HTTPException as http_error:
        log_body = LoggerModel(http_error.status_code, endpoint, http_error.detail, "error")    
        log.set_log_message(logger, log_body)
        raise http_error
    except Exception as error:
        error_message = f"Erro interno : {error}"
        log_body = LoggerModel(500, endpoint, error_message, "error")    
        log.set_log_message(logger, log_body)
        raise HTTPException(
            status_code=500,
            detail=error_message
        )
