import os
from dotenv import load_dotenv
from pydantic import PostgresDsn

load_dotenv()

# База данных
DATABASE_URL: PostgresDsn = os.getenv("DATABASE_URL")
ASYNC_DATABASE_URL: PostgresDsn = os.getenv("ASYNC_DATABASE_URL")

# Секреты для FastAPI Users
SECRET: str = os.getenv("SECRET_KEY")

# Настройки для токенов
RESET_PASSWORD_SECRET: str = os.getenv("RESET_PASSWORD_SECRET", "DEFAULT_RESET_SECRET")
VERIFICATION_SECRET: str = os.getenv("VERIFICATION_SECRET", "DEFAULT_VERIFY_SECRET")

# Redis
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")