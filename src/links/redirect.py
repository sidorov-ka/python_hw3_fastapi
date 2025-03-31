from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from src.database import get_db
from src.models import Link

router = APIRouter()


@router.get(
    "/{short_code}",
    response_class=RedirectResponse,
    status_code=302,
    include_in_schema=False,
    summary="Redirect by Short Code",
    description="Перенаправляет пользователя на оригинальную ссылку по короткому коду. "
                "Если ссылка истекла — вернёт 410. Если не найдена — 404.",
)
def redirect_to_original(
    short_code: str,
    db: Session = Depends(get_db),
):
    """
    Редирект по короткому коду. Обновляет статистику:
    - увеличивает счётчик `clicks`
    - обновляет поле `last_accessed`

    Возвращает:
    - `302 Found` — редирект на оригинальную ссылку
    - `404 Not Found` — если ссылка не существует
    - `410 Gone` — если ссылка истекла
    """
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    if link.expires_at and link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Link has expired")

    link.clicks += 1
    link.last_accessed = datetime.utcnow()
    db.commit()

    return RedirectResponse(url=link.original_url)