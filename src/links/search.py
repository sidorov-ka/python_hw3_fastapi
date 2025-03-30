from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from src.database import get_db
from src.models import Link
from .schemas import LinkInfo

router = APIRouter()

@router.get("/search-by-url", response_model=List[LinkInfo])
def search_links_by_original_url(
    original_url: str = Query(..., description="Оригинальный URL для поиска"),
    db: Session = Depends(get_db)
):
    """
    Поиск всех коротких ссылок по оригинальному URL (игнорируя регистр и хвостовые слеши).
    """
    normalized_url = original_url.rstrip("/")

    links = db.query(Link).filter(
        func.lower(func.trim(Link.original_url, "/")) == func.lower(normalized_url)
    ).all()

    if not links:
        raise HTTPException(status_code=404, detail="No links found for this original URL")

    return [
        LinkInfo(
            short_url=f"/{link.short_code}",
            original_url=link.original_url,
            expires_at=link.expires_at
        ) for link in links
    ]
