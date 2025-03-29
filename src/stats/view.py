from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Link
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class LinkStats(BaseModel):
    original_url: str
    created_at: datetime
    clicks: int
    last_accessed: datetime | None

    class Config:
        from_attributes = True

@router.get("/links/{short_code}/stats", response_model=LinkStats)
def get_link_stats(short_code: str, db: Session = Depends(get_db)) -> LinkStats:
    """
    Возвращает статистику по ссылке:
    - оригинальный URL
    - дата создания
    - количество переходов
    - дата последнего использования
    """
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    return link
