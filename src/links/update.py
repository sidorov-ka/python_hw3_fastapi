from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.models import Link, User
from src.auth.manager import fastapi_users
from src.links.schemas import LinkUpdate, LinkInfo

router = APIRouter()


@router.put("/links/{short_code}", response_model=LinkInfo)
def update_short_link(
    short_code: str,
    payload: LinkUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(fastapi_users.current_user(optional=True)),
):
    """
    Обновляет информацию о ссылке.

    Только авторизованный пользователь, являющийся владельцем ссылки, может её изменить.
    Анонимные ссылки изменить нельзя.
    """
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    if not link.user_id:
        raise HTTPException(status_code=403, detail="Anonymous links cannot be updated")

    if not current_user or current_user.id != link.user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this link")

    if payload.original_url is not None:
        link.original_url = str(payload.original_url)

    if payload.custom_alias:
        if db.query(Link).filter_by(custom_alias=payload.custom_alias).first():
            raise HTTPException(status_code=400, detail="Alias already in use")
        link.custom_alias = payload.custom_alias
        link.short_code = payload.custom_alias

    if payload.expires_at is not None:
        link.expires_at = payload.expires_at

    db.commit()
    db.refresh(link)

    return LinkInfo(
        short_url=f"{link.short_code}",
        original_url=link.original_url,
        expires_at=link.expires_at,
    )
