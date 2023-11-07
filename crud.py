from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
            email=user.email, 
            hashed_password=user.password,
            phone=user.phone,
            full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def register_user(db: Session, user):
    db_user = models.User(
            email=user['email'], 
            hashed_password=user['password'],
            phone=user['phone'],
            full_name=user['full_name'])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def upload_profile(db: Session, user, profile_pic):
    db_user = models.Profile_Picture(
            user_id=user['id'], 
            profile_pic=profile_pic)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user