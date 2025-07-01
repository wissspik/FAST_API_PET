from sqlalchemy.orm import DeclarativeBase, relationship, Mapped,mapped_column
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,LargeBinary
from datetime import datetime
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
class Base(DeclarativeBase):
    pass

class Profile(Base):
    __tablename__ = 'profile'
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=False, index=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=False, index=True, nullable=True)
    surname: Mapped[str] = mapped_column(unique=False, index=True, nullable=True)
    patronymic: Mapped[str] = mapped_column(unique=False, index=True, nullable=True)
    gender: Mapped[str] = mapped_column(
        PGEnum('male', 'female', 'other', name='gender_enum'),
        nullable=True
    )
    city: Mapped[str] = mapped_column(unique=False, index=True, nullable=True)
    age: Mapped[int] = mapped_column(unique=False, index=True, nullable=True)

    photos = relationship(
        "Photo",
        back_populates="profile",
        cascade="all, delete-orphan"
    )

class Photo(Base):
    __tablename__ = 'photo'
    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey('profile.id', ondelete='SET NULL', onupdate='CASCADE'),
        nullable=False
    )
    file_name: Mapped[str]    = mapped_column(nullable=False)
    mime_type: Mapped[str]    = mapped_column(nullable=False)
    file_size: Mapped[int]    = mapped_column(nullable=False)
    file: Mapped[bytes]       = mapped_column(LargeBinary, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    profile = relationship("Profile", back_populates="photos")