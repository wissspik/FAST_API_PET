from sqlalchemy.orm import DeclarativeBase, relationship, Mapped,mapped_column
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,LargeBinary
from datetime import datetime
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
class Base(DeclarativeBase):
    pass

class Profile(Base):
    __tablename__ = 'profile'
    id :Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(unque = False,index = True, nullable = False)
    surname: Mapped[str] = mapped_column(unque = False,index = True, nullable = False)
    patronymic: Mapped[str] = mapped_column(unque = False,index = True, nullable = True)
    gender: Mapped[str] = mapped_column(
        PGEnum('male', 'female', 'other', name='gender_enum'),
        nullable=False
    )
    city: Mapped[str] = mapped_column(unque = False,index = True, nullable = True)
    age:Mapped[int] = mapped_column(unque = False,index = True, nullable = True)

    photos =  relationship("Photo",back_populates="profile",cascade="all, delete-orphan")

class Photo(Base):
    __tablename__ = 'photo'

    id: Mapped[int] = mapped_column(primary_key=True)

    picture:Mapped[int] = mapped_column(ForeignKey('profile.id', ondelete='SET NULL', onupdate='CASCADE'),nullable=False)

    file_name: Mapped[str] = mapped_column(nullable=False,index=False,unique=False)
    mime_type: Mapped[str] = mapped_column(nullable=False,index=False,unique=False)
    file_size: Mapped[int] = mapped_column(nullable=False,index=False,unique=False)
    file: Mapped[bytes] = mapped_column(LargeBinary,nullable=False,unique= False,index=False)
    uploaded_at: Mapped[datetime] = mapped_column(default=datetime.now,nullable=False)
    profile = relationship(
        "Profile",
        back_populates="photos"
    )
