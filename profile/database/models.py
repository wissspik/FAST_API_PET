from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from sqlalchemy.dialects.postgresql import ENUM as PGEnum
class Base(DeclarativeBase):
    pass

class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    name = Column(String(100),unque = False,index = True, nullable = False)
    surname = Column(String(100),unque = False,index = True, nullable = False)
    patronymic = Column(String(100),unque = False,index = True, nullable = True)
    gender = Column(
        PGEnum('male','female','other'),name='gender_enum',nullable=False)
    city = Column(String(100),unque = False,index = True, nullable = True)
    age = Column(Integer,unque = False,index = True, nullable = True)

    photos =  relationship("Photo",back_populates="profile",cascade="all, delete-orphan")

class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)

    picture = Column(Integer,ForeignKey('profile.id', ondelete='SET NULL', onupdate='CASCADE'),nullable=False)

    profile = relationship(
        "Profile",
        back_populates="photos"
    )