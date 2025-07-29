from fastapi import APIRouter, HTTPException
from app.api.v1.endpoint_categoria import dados_csv
from app.models.logger import LoggerModel
from app.utils.app_logger import AppLogger

router = APIRouter()

log = AppLogger()
logger = log.create_logger(__name__)

@router.get("/api/v1/health")
async def health():
    endpoint = router.url_path_for("health")
    try:
        if dados_csv.empty:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
            
        log_body = LoggerModel(200, endpoint, "Records found in books.CSV")    
        log.set_log_message(logger, log_body)
        return {
            "Success": True,
            "API status": 200,
            "Data": {
                "Total records found in books.CSV": len(dados_csv)
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
