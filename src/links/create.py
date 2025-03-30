from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from src.database import get_db
from src.models import Link
from .schemas import LinkCreate, LinkInfo

router = APIRouter()


@router.post("/links/shorten", response_model=LinkInfo)
def create_short_link(
    payload: LinkCreate,
    request: Request,
    db: Session = Depends(get_db)
) -> LinkInfo:
    """
    Генерация короткой ссылки на основе оригинальной URL.
    Если передан `custom_alias`, он будет использоваться как часть короткой ссылки.
    """

    # Проверка, не занят ли custom_alias
    if payload.custom_alias:
        existing = db.query(Link).filter_by(custom_alias=payload.custom_alias).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Alias already in use"
            )
        short_code = payload.custom_alias
    else:
        # Генерация уникального short_code
        short_code = uuid4().hex[:6]
        while db.query(Link).filter_by(short_code=short_code).first():
            short_code = uuid4().hex[:6]

    print("Сохраняем ссылку с URL:", payload.original_url)
    # Создание объекта ссылки
    link = Link(
        original_url=str(payload.original_url),  # HttpUrl → str
        short_code=short_code,
        custom_alias=payload.custom_alias,
        expires_at=payload.expires_at,
        created_at=datetime.utcnow()
    )

    # Сохраняем в базу
    db.add(link)
    db.commit()
    db.refresh(link)

    # Генерируем полный URL
    base_url = str(request.base_url).rstrip("/")
    short_url = f"{base_url}/{short_code}"

    return LinkInfo(
        short_url=short_url,
        original_url=link.original_url,
        expires_at=link.expires_at
    )