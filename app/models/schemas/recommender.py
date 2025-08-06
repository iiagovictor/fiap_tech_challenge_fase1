from pydantic import BaseModel
from typing import List

class RecomendarRequest(BaseModel):
    titulo_livro: str

class RecomendacoesResponse(BaseModel):
    livro_base: str
    recomendacoes: List[str]