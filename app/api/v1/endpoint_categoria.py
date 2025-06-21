from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_categories():
    return  "Somente para evitar erros"


@router.get("/api/v1/categories")
async def get_categories():
    return  "Teste"