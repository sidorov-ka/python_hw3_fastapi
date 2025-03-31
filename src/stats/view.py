from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from src.database import get_db
from src.models import Link, User
from src.auth.manager import fastapi_users

from pydantic import BaseModel

router = APIRouter()

class LinkStats(BaseModel):
    original_url: str
    created_at: datetime
    clicks: int
    last_accessed: Optional[datetime]

    class Config:
        from_attributes = True

@router.get("/links/{short_code}/stats", response_model=LinkStats)
def get_link_stats(
    short_code: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(fastapi_users.current_user(optional=True))
) -> LinkStats:
    """
    Статистика по короткой ссылке.
    Открыта только автору, если ссылка привязана к пользователю.
    """
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    # 🔐 Если ссылка принадлежит пользователю, проверяем доступ
    if link.user_id:
        if not current_user or current_user.id != link.user_id:
            raise HTTPException(status_code=403, detail="Access denied")

    return link
