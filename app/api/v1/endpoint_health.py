from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/health")
async def get_status():
    return 'Teste'