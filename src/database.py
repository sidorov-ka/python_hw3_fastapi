# Импортируем create_engine для подключения к базе и sessionmaker для создания сессий
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Для загрузки переменных окружения из .env
from dotenv import load_dotenv
import os

# Импортируем общий Base (декларативная база для моделей)
from src.db_base import Base

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем строку подключения из переменной окружения
# Пример: postgresql://postgres:your_password@localhost:5432/url_shortener
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Создаём движок SQLAlchemy — объект, управляющий подключением к БД
engine = create_engine(DATABASE_URL)

# Создаём фабрику сессий — будет использоваться в эндпоинтах FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Функция для инициализации таблиц в базе данных
# Импорт моделей выполняется здесь (внутри), чтобы избежать циклических импортов
def init_db():
    from src.models import User, Link
    # Создаём таблицы в базе на основе всех моделей, унаследованных от Base
    Base.metadata.create_all(bind=engine)


# Зависимость FastAPI — создаёт сессию БД на каждый запрос
# Используется в хендлерах через Depends(get_db)
def get_db():
    db = SessionLocal()
    try:
        yield db  # возвращаем сессию
    finally:
        db.close()  # обязательно закрываем после запроса
