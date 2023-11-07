from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)


class Profile_Picture(Base):
    __tablename__ = 'profile_picture'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    profile_pic = Column(String)

