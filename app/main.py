from fastapi import FastAPI
from app.config import Config
from app.api import root
from app.api.v1 import (
    books,
    categories,
    health,
    stats,
    users,
    auth,
    scraping,
    price_range
)

app = FastAPI(
    title=Config.TITLE,
    version=Config.VERSION,
    debug=Config.DEBUG,
    description=Config.DESCRIPTION
)

app.include_router(root.router)
app.include_router(categories.router)
app.include_router(health.router)
app.include_router(stats.router)
app.include_router(price_range.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(scraping.router)
