from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.models import Link, User
from src.auth.manager import fastapi_users

router = APIRouter()

@router.delete("/links/{short_code}", status_code=204)
def delete_short_link(
    short_code: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(fastapi_users.current_user(optional=True))
):
    """
    Удаляет ссылку по short_code.

    Только авторизованный пользователь, являющийся автором, может удалить свою ссылку.
    Анонимные ссылки — удалить нельзя.
    """
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    if not link.user_id:
        raise HTTPException(status_code=403, detail="Anonymous links cannot be deleted")

    if not current_user or current_user.id != link.user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this link")

    db.delete(link)
    db.commit()
