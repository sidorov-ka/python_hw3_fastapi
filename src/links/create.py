from datetime import datetime
from uuid import uuid4
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Link, User
from src.links.schemas import LinkCreate, LinkInfo
from src.auth.manager import fastapi_users

router = APIRouter()

@router.post("/links/shorten", response_model=LinkInfo)
def create_short_link(
    payload: LinkCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(fastapi_users.current_user(optional=True))
) -> LinkInfo:
    """
    Создаёт короткую ссылку. Поддерживает кастомные alias и срок жизни ссылки.
    Авторизованный пользователь будет сохранён как владелец ссылки.
    """
    if payload.custom_alias:
        if db.query(Link).filter_by(custom_alias=payload.custom_alias).first():
            raise HTTPException(status_code=400, detail="Alias already in use")
        short_code = payload.custom_alias
    else:
        short_code = uuid4().hex[:6]
        while db.query(Link).filter_by(short_code=short_code).first():
            short_code = uuid4().hex[:6]

    new_link = Link(
        original_url=str(payload.original_url),
        short_code=short_code,
        custom_alias=payload.custom_alias,
        expires_at=payload.expires_at,
        created_at=datetime.utcnow(),
        user_id=current_user.id if current_user else None
    )

    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    short_url = f"{str(request.base_url).rstrip('/')}/{short_code}"

    return LinkInfo(
        short_url=short_url,
        original_url=new_link.original_url,
        expires_at=new_link.expires_at
    )
