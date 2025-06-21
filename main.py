from fastapi import FastAPI

app = FastAPI(
    title="Our FastAPI API",
    version="1.0.0",
    description="API de Consultas de Livros com FASTAPI"
)


@app.get("/")
async def home():
    return "Página Inicial!"
