from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional

from src.database import Base
from fastapi_users.db import SQLAlchemyBaseUserTable


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    links = relationship("Link", back_populates="user")


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_url: Mapped[str] = mapped_column(Text, nullable=False)
    short_code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    custom_alias: Mapped[Optional[str]] = mapped_column(String(30), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    last_accessed: Mapped[Optional[datetime]] = mapped_column(DateTime)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"))
    user = relationship("User", back_populates="links")
