from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Link
from .schemas import UpdateLinkRequest
router = APIRouter()

@router.put("/links/{short_code}")
def update_original_url(
    short_code: str,
    payload: UpdateLinkRequest,
    db: Session = Depends(get_db)
):
    """
    Обновление оригинального URL по short_code.
    """
    link = db.query(Link).filter_by(short_code=short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    link.original_url = str(payload.new_url)
    db.commit()

    return {
        "message": "Original URL updated successfully",
        "short_code": short_code,
        "new_url": payload.new_url
    }
