import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

# Загрузка переменных окружения
load_dotenv()

# Создаём базу для моделей
Base = declarative_base()

# ⏬ Асинхронная часть
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

ASYNC_DATABASE_URL = os.getenv(
    "ASYNC_DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost/dbname"
)

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# 🔁 Синхронная часть (используется FastAPI Users)
from sqlalchemy import create_engine as sync_create_engine
from sqlalchemy.orm import sessionmaker as sync_sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/dbname"
)

engine = sync_create_engine(DATABASE_URL)
SessionLocal = sync_sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Инициализация БД (если нужно вручную создать таблицы)
async def init_db():
    async with async_engine.begin() as conn:
        from src.models import Base  # ✅ Локальный импорт — безопасен
        await conn.run_sync(Base.metadata.create_all)
