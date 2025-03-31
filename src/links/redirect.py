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
    summary="Redirect by short code",
    description="Перенаправляет пользователя по короткому коду. Учитывает срок жизни ссылки.",
)
def redirect_to_original(
    short_code: str,
    db: Session = Depends(get_db),
):
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    if link.expires_at and link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Link has expired")

    # Обновление статистики
    link.clicks += 1
    link.last_accessed = datetime.utcnow()
    db.commit()

    return RedirectResponse(url=link.original_url)
