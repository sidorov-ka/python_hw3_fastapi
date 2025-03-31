from fastapi import APIRouter, HTTPException, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from src.database import get_db
from src.models import Link
from src.links.schemas import LinkInfo

router = APIRouter()

@router.get("/links/search", response_model=List[LinkInfo])
def search_links_by_original_url(
    request: Request,
    original_url: str = Query(..., description="Оригинальный URL для поиска"),
    db: Session = Depends(get_db)
):
    """
    Поиск всех коротких ссылок по оригинальному URL (без учёта регистра, убирая слеш).
    """
    normalized_url = original_url.rstrip("/")
    cleaned_url = normalized_url.replace("/", "").lower()

    links = db.query(Link).filter(
        func.lower(func.replace(Link.original_url, "/", "")) == cleaned_url
    ).all()

    if not links:
        raise HTTPException(status_code=404, detail="No links found for this original URL")

    base_url = str(request.base_url).rstrip("/")

    return [
        LinkInfo(
            short_url=f"{base_url}/{link.short_code}",
            original_url=link.original_url,
            expires_at=link.expires_at
        ) for link in links
    ]
