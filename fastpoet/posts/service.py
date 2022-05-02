from sqlalchemy.orm import Session

from . import models, schemas


def get_posts(db: Session):
    return db.query(models.Post).all()


def create_post(db: Session, item: schemas.PostCreate):
    db_item = models.Post(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
