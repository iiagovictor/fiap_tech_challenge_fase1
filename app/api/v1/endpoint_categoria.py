from fastapi import APIRouter, HTTPException
from app.models.logger import LoggerModel
from app.utils.app_logger import AppLogger
from app.utils.helpers import get_csv_data, get_unique_items

router = APIRouter()
dados_csv = get_csv_data('./data/books.csv')
# dados_csv = get_csv_data('data/books_empty.csv')
# dados_csv = get_csv_data('data/books_without_data.csv')

log = AppLogger()
logger = log.create_logger(__name__)

@router.get("/")
async def home():
    return "Somente para evitar erros"


@router.get("/api/v1/categories")
async def get_categories():
    endpoint = router.url_path_for("get_categories")
    try:
        dados_filtrados = get_unique_items(dados_csv, "category")
        if len(dados_filtrados) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        
        log_body = LoggerModel(200, endpoint, "Categorias retornadas com sucesso.")    
        log.set_log_message(logger, log_body)
        
        return {
            "Success": True,
            "Message": "Categorias retornadas com sucesso.",
            "Data": {
                "Categories": dados_filtrados
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
            status_code= 500,
            detail= error_message
        )
