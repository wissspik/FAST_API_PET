from sqlalchemy import Integer, String,DateTime,ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
import enum
from sqlalchemy import Enum

class Role(enum.Enum):
    admin = "admin"
    user = "user"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, index=True, unique=True
    )
    login: Mapped[str] = mapped_column(
        String(30), index=True, nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column(
        String(136), nullable=False, unique=False, index=True
    )
    role: Mapped[Role] = mapped_column(
        Enum(Role), nullable=False, unique=False, index=False
    )
    email: Mapped[str] = mapped_column(
        String(120), nullable=True, unique=True, index=True
    )
    phone: Mapped[str] = mapped_column(
        String(11), unique=True, nullable=True, index=True
    )
    articles: Mapped[list["Article"]] = relationship(
        back_populates="user",
        cascade="all"
    )
class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, index=True, unique=True
    )
    # Внешний ключ указывает на User
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(256), index=True, nullable=False, unique=False
    )
    content: Mapped[str] = mapped_column(
        String(1500), nullable=False, unique=False
    )
    created_at : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    interests : Mapped[str] = mapped_column(
        String(256), index=True, nullable=False, unique=True
    )
    # обратная связь
    user: Mapped["User"] = relationship(
        back_populates="articles"
    )
