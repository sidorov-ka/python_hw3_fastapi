from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from src.database import get_db
from src.models import Link

router = APIRouter()

@router.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    """
    Редирект по короткой ссылке.
    Если ссылка найдена и не истекла — редиректим.
    Также обновляем количество переходов и дату последнего использования.
    """
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    # Проверка срока действия
    if link.expires_at and link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Link has expired")

    # Обновляем статистику
    link.clicks += 1
    link.last_accessed = datetime.utcnow()
    db.commit()

    return RedirectResponse(link.original_url)