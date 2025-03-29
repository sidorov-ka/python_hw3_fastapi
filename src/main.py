from fastapi import FastAPI

from src.links.create import router as create_router
from src.links.redirect import router as redirect_router
from src.links.delete import router as delete_router
from src.links.update import router as update_router
from src.stats.view import router as stats_router

app = FastAPI(
    title="URL Shortener",
    description="Сервис для сокращения ссылок, отслеживания статистики и управления ими.",
    version="1.0.0"
)

# Подключение роутеров с тегами
app.include_router(create_router, tags=["Links"])
app.include_router(redirect_router, tags=["Links"])
app.include_router(delete_router, tags=["Links"])
app.include_router(update_router, tags=["Links"])
app.include_router(stats_router, tags=["Stats"])
