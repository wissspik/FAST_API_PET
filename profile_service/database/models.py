from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        LargeBinary, String, func,)
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Profile(Base):
    __tablename__ = "profile_service"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=False, index=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=False, index=True, nullable=True)
    surname: Mapped[str] = mapped_column(unique=False, index=True, nullable=True)
    patronymic: Mapped[str] = mapped_column(unique=False, index=True, nullable=True)
    gender: Mapped[str] = mapped_column(
        PGEnum("male", "female", "other", name="gender_enum"), nullable=True
    )
    city: Mapped[str] = mapped_column(unique=False, index=True, nullable=True)
    age: Mapped[int] = mapped_column(unique=False, index=True, nullable=True)

    photos = relationship(
        "Photo",
        back_populates="profile_service",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Photo(Base):
    __tablename__ = "photo"
    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile_service.id", ondelete="CASCADE"),
        nullable=False,
        passive_deletes=True,
        unique=True,
    )
    file_name: Mapped[str] = mapped_column(nullable=False)
    mime_type: Mapped[str] = mapped_column(nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False)
    file: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    profile_service = relationship("Profile", back_populates="photos")
