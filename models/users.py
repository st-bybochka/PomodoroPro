from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class UserProfile(Base):
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
