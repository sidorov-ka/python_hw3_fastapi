from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Link

router = APIRouter()

@router.delete("/links/{short_code}", status_code=204)
def delete_short_link(short_code: str, db: Session = Depends(get_db)):
    """
    Удаление короткой ссылки по short_code.
    """
    link = db.query(Link).filter_by(short_code=short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    db.delete(link)
    db.commit()
