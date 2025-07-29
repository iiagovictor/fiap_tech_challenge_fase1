from fastapi import APIRouter, HTTPException
from app.models.logger import LoggerModel
from app.utils.app_logger import AppLogger
from app.utils.helpers import get_unique_items
from app.api.v1.endpoint_categoria import dados_csv

router = APIRouter()

log = AppLogger()
logger = log.create_logger(__name__)

@router.get("/api/v1/books")
async def get_books():
    endpoint = router.url_path_for("get_books")
    
    try:
        livros_filtrados = get_unique_items(dados_csv, "title")
        if len(livros_filtrados) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
            
        log_body = LoggerModel(200, endpoint, "Livros retornadas com sucesso.")    
        log.set_log_message(logger, log_body)
        return {
            "Success": True,
            "Message": "Livros retornadas com sucesso.",
            "Data": {
                "Livros": livros_filtrados
            }
        }
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
