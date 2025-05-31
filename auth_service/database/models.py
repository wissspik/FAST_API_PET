from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String,Integer

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key = True,
        nullable = False,
        index = True,
        unique = True
    )
    login: Mapped[str] = mapped_column(
        String(30),
        index = True,
        nullable = False,
        unique = True
    )
    password: Mapped[str]   = mapped_column(
        String(136),
        nullable = False,
        unique = False,
        index = True
    )
    role: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=False,
        index = False
    )
    email: Mapped[str] = mapped_column(
        String(120),
        nullable=True,
        unique=True,
        index=True
    )
    phone: Mapped[str] = mapped_column(
        String(11),
        unique=True,
        nullable = True,
        index=True
    )
