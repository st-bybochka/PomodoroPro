from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Categories(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
