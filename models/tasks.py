from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Tasks(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id', ondelete='CASCADE'), nullable=False)