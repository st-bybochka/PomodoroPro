from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class UserProfile(Base):
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[Optional[str]] = mapped_column(nullable=True)
    password: Mapped[Optional[str]] = mapped_column(nullable=True)
    google_access_token: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    google_id: Mapped[Optional[str]] = mapped_column(nullable=True)  # Добавлено поле
