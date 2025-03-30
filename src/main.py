from fastapi import FastAPI

from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Link

from src.links.create import router as create_router
from src.links.redirect import router as redirect_router
from src.links.delete import router as delete_router
from src.links.update import router as update_router
from src.links.search import router as search_router
from src.stats.view import router as stats_router

app = FastAPI(
    title="URL Shortener",
    description="Сервис для сокращения ссылок, отслеживания статистики и управления ими.",
    version="1.0.0"
)

# Подключение роутеров
app.include_router(create_router, tags=["Links"])
app.include_router(redirect_router, tags=["Links"])
app.include_router(delete_router, tags=["Links"])
app.include_router(update_router, tags=["Links"])
app.include_router(search_router, tags=["Links"])
app.include_router(stats_router, tags=["Stats"])

@app.on_event("startup")
def show_all_links_on_startup():
    db: Session = next(get_db())
    links = db.query(Link).all()
    print("\n Ссылки в базе при старте:")
    for link in links:
        print(f"- [{link.short_code}] {link.original_url}")
