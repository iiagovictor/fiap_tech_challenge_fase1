from fastapi import APIRouter, HTTPException
from app.api.v1.endpoint_categoria import dados_csv
from app.models.logger import LoggerModel
from app.utils import helpers
from app.utils.app_logger import AppLogger

router = APIRouter()

log = AppLogger()
logger = log.create_logger(__name__)

@router.get('/api/v1/stats/overview')
async def get_overview_data():
    endpoint = router.url_path_for("get_overview_data")
    try:
        if len(dados_csv) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
            
        log_body = LoggerModel(200, endpoint, "Overview sobre os dados registrados.")    
        log.set_log_message(logger, log_body)
        return {
            "Success": True,
            "Message": "Overview sobre os dados.",
            "Data": {
                "Total": len(dados_csv),
                "Average": round(dados_csv['price_including_tax'].mean(), 2),
                "Ratings distribution": {
                    "Rating One": helpers.get_rating(
                        dados_csv, 'review_rating', 1, 0
                    ),
                    "Rating Two": helpers.get_rating(
                        dados_csv, 'review_rating', 2, 0
                    ),
                    "Rating Three": helpers.get_rating(
                        dados_csv, 'review_rating', 3, 0
                    ),
                    "Rating Four": helpers.get_rating(
                        dados_csv, 'review_rating', 4, 0
                    ),
                    "Rating Five": helpers.get_rating(
                        dados_csv, 'review_rating', 5, 0
                    ),
                }
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
