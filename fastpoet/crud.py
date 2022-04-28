from sqlalchemy.orm import Session

from fastpoet import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username
    ).first()


# лимиты на количество записей
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # тут видимо будет защита паролей.
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        username=user.username, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# лимиты на количество записей
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_item = models.Post(**post.dict(), author_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
