from sqlalchemy import Boolean, Column, Integer, String
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.ext.declarative import declarative_base

# Базовый класс для моделей
Base = declarative_base()

class User(SQLAlchemyBaseUserTable, Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
