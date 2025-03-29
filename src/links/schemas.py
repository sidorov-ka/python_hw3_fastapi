from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime


class LinkCreate(BaseModel):
    """
    Схема для создания короткой ссылки.
    """
    original_url: HttpUrl = Field(..., description="Оригинальный URL, который нужно сократить.")
    custom_alias: Optional[str] = Field(None, description="Произвольный alias для короткой ссылки (опционально).")
    expires_at: Optional[datetime] = Field(None, description="Время истечения ссылки в формате ISO (опционально).")


class LinkInfo(BaseModel):
    """
    Схема ответа пользователю после создания короткой ссылки.
    """
    short_url: str = Field(..., description="Сформированная короткая ссылка.")
    original_url: HttpUrl = Field(..., description="Оригинальный URL.")
    expires_at: Optional[datetime] = Field(None, description="Срок действия ссылки (если указан).")


class UpdateLinkRequest(BaseModel):
    """
    Схема для обновления оригинального URL у существующей короткой ссылки.
    """
    new_url: HttpUrl = Field(..., description="Новый оригинальный URL, на который будет вести короткая ссылка.")
