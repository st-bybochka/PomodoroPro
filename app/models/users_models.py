from typing import Optional
from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database import Base


class UserProfile(Base):
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    password: Mapped[Optional[str]] = mapped_column(nullable=True)
    login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    block_until: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    google_id: Mapped[Optional[str]] = mapped_column(nullable=True)