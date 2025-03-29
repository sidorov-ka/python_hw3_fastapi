from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime


# Входная схема для создания короткой ссылки
class LinkCreate(BaseModel):
    original_url: HttpUrl
    custom_alias: Optional[str] = None
    expires_at: Optional[datetime] = None


# Ответ пользователю после создания ссылки
class LinkInfo(BaseModel):
    short_url: str
    original_url: HttpUrl
    expires_at: Optional[datetime] = None
