from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List

from src.db_base import Base


# Модель пользователя — таблица "user"
# Используется для регистрации, авторизации и привязки ссылок
class User(Base):
    __tablename__ = "user"

    # Уникальный идентификатор пользователя
    id: Mapped[int] = mapped_column(primary_key=True)

    # Email пользователя, по нему будет происходить логин
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    # Хэшированный пароль
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)

    # Флаг — активен ли аккаунт
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Флаг — является ли пользователь суперюзером
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Дополнительный логин или псевдоним
    username: Mapped[str] = mapped_column(String, unique=True, index=True)

    # Связь один-ко-многим: пользователь → ссылки
    links: Mapped[List["Link"]] = relationship(back_populates="user")


# Модель короткой ссылки — таблица "links"
class Link(Base):
    __tablename__ = "links"

    # Уникальный ID ссылки
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Оригинальный (длинный) URL
    original_url: Mapped[str] = mapped_column(Text, nullable=False)

    # Уникальный сгенерированный код (пример: "aBcD1")
    short_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)

    # Кастомный алиас от пользователя (если указан)
    custom_alias: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)

    # Дата создания
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Срок жизни ссылки (если задан)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Последний переход по ссылке
    last_accessed: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Счётчик кликов по короткой ссылке
    clicks: Mapped[int] = mapped_column(Integer, default=0)

    # ID пользователя, создавшего ссылку (может быть null для анонимных)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)

    # ORM-связь: ссылка знает, кто её создал
    user: Mapped[Optional[User]] = relationship(back_populates="links")
