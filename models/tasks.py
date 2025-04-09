from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Tasks(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]