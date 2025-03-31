from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from src.database import get_db
from src.models import Link, User
from src.auth.manager import fastapi_users
from src.links.schemas import LinkUpdate, LinkInfo

router = APIRouter()

@router.put("/links/{short_code}", response_model=LinkInfo)
def update_link(
    short_code: str,
    payload: LinkUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(fastapi_users.current_user(optional=True))
):
    """
    Обновление короткой ссылки (original_url, alias, expires_at).
    Только владелец может обновлять свою ссылку.
    """
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    if not link.user_id:
        raise HTTPException(status_code=403, detail="Anonymous links cannot be updated")

    if not current_user or current_user.id != link.user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this link")

    # Обновляем поля, если переданы
    if payload.original_url:
        link.original_url = str(payload.original_url)

    if payload.custom_alias:
        # Проверка уникальности
        exists = db.query(Link).filter(Link.custom_alias == payload.custom_alias, Link.id != link.id).first()
        if exists:
            raise HTTPException(status_code=400, detail="Custom alias already in use")
        link.custom_alias = payload.custom_alias
        link.short_code = payload.custom_alias  # меняем и short_code тоже

    if payload.expires_at:
        if payload.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Expiration date must be in the future")
        link.expires_at = payload.expires_at

    db.commit()
    db.refresh(link)

    return LinkInfo(
        short_url=f"http://localhost:8000/{link.short_code}",
        original_url=link.original_url,
        expires_at=link.expires_at
    )
