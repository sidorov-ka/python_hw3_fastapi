from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

# Получаем строку подключения из .env
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')

# Подключение к PostgreSQL
engine = create_engine(DATABASE_URL)

# Сессия
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовая модель
Base = declarative_base()

# Создание таблиц
def init_db():
    from .models import User  # подключим все модели, которые хотим создать
    Base.metadata.create_all(bind=engine)

# Зависимость для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
