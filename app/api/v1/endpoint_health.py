from fastapi import APIRouter, HTTPException
from app.api.v1.endpoint_categoria import dados_csv

router = APIRouter()

@router.get("/api/v1/health")
async def health():
    try:
        if dados_csv.empty:
            raise HTTPException(
                status_code=400,
                detail="Arquivo CSV não está populado."
            )
        return {
            "Success": True,
            "API status": 200,
            "Data": {
                "Total records found in books.CSV": len(dados_csv)
                }
        }
    
    except HTTPException as http_error:
        raise http_error 

    except Exception as error:
        raise   HTTPException(
            status_code=500,
            detail=f"Erro interno {error}"
        )