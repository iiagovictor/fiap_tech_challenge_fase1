from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from app.api.v1.auth import get_current_user
from app.models.schemas.scraping import (
    ScrapingTriggerResponse,
    ScrapingStatusResponse,
)
from app.utils.scraping import BooksToScrape
from app.models.databases.scraping import ScrapingRequest
from app.models.databases.base import SessionLocal
import logging
import threading
import uuid

router = APIRouter(tags=["Scraping"])

scraping_lock = threading.Lock()


def run_scraping_job(request_id):
    session = SessionLocal()
    try:
        req = session.query(ScrapingRequest).filter_by(id=request_id).first()
        if req:
            req.status = "running"
            req.message = "Scraping em andamento."
            session.commit()
        scraper = BooksToScrape()
        books = scraper.get_books()
        scraper.save_books_to_csv(books)
        scraper.save_books_to_json(books)
        if req:
            req.status = "done"
            req.message = f"Scraping finalizado com sucesso. Livros coletados: {len(books)}"  # noqa: E501
            session.commit()
        logging.info(
            f"Scraping finalizado com sucesso. Livros coletados: {len(books)}"
            )
    except Exception as e:
        if req:
            req.status = "error"
            req.message = str(e)
            session.commit()
        logging.error(f"Erro ao executar o scraping: {e}")
    finally:
        session.close()
        if scraping_lock.locked():
            scraping_lock.release()


@router.post("/api/v1/scraping/trigger", response_model=ScrapingTriggerResponse, status_code=201)  # noqa: E501
async def trigger_scraping(background_tasks: BackgroundTasks, user=Depends(get_current_user)):  # noqa: E501
    """### 🚀 Trigger Web Scraping
    Executa o script de scraping em background e retorna imediatamente.
    Salva os resultados em CSV e JSON na pasta data/.
    Garante que apenas uma execução ocorra por vez.
    Retorna um id para consulta do status.
    """  # noqa: E501
    if scraping_lock.locked():
        raise HTTPException(
            status_code=409,
            detail="Já existe um scraping em andamento."
            )
    request_id = str(uuid.uuid4())
    session = SessionLocal()
    scraping_req = ScrapingRequest(
        id=request_id,
        status="pending",
        message="Scraping aguardando execução.",
        trigger_by_user=user["sub"]
    )
    session.add(scraping_req)
    session.commit()
    session.close()
    scraping_lock.acquire()
    background_tasks.add_task(run_scraping_job, request_id)
    return {
        "success": True,
        "message": "Scraping iniciado em background.",
        "data": {
            "status": "pending",
            "id": request_id,
            "trigger_by_user": user["sub"]
        }
    }


@router.get("/api/v1/scraping/status/{request_id}", response_model=ScrapingStatusResponse)  # noqa: E501
def get_scraping_status(request_id: str, user=Depends(get_current_user)):
    """### 📊 Status do Scraping
    Consulta o status de uma solicitação de scraping pelo id.
    """  # noqa: E501
    session = SessionLocal()
    req = session.query(ScrapingRequest).filter_by(id=request_id).first()
    session.close()
    if not req:
        raise HTTPException(
            status_code=404,
            detail="ID de scraping não encontrado."
            )
    return {
        "success": True,
        "message": req.message,
        "data": {
            "status": req.status,
            "id": req.id,
            "created_at": req.created_at,
            "updated_at": req.updated_at,
            "trigger_by_user": req.trigger_by_user
        },
    }
