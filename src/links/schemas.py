from typing import Optional
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime


class LinkCreate(BaseModel):
    original_url: HttpUrl
    custom_alias: Optional[str] = Field(
        default=None,
        max_length=30,
        pattern="^[a-zA-Z0-9_-]+$"
    )
    expires_at: Optional[datetime] = None


class LinkInfo(BaseModel):
    short_url: HttpUrl
    original_url: HttpUrl
    expires_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class LinkUpdate(BaseModel):
    original_url: Optional[HttpUrl] = None
    custom_alias: Optional[str] = Field(
        default=None,
        max_length=30,
        pattern="^[a-zA-Z0-9_-]+$"
    )
    expires_at: Optional[datetime] = None
