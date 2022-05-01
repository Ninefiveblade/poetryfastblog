"""Тестирование"""
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from fastpoet import crud, models, schemas
from fastpoet.database import SessionLocal, engine
from fastpoet.routers import router

models.Base.metadata.create_all(bind=engine)


def create_app():
    """Application Initialization"""
    app = FastAPI()
    app.include_router(router)
    return app


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = create_app()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def users_get(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def user_get(user_id: int, db: Session = Depends(get_db)):
    users = crud.get_user(db, user_id)
    return users


@app.get("/posts/", response_model=list[schemas.Post])
def posts_get(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return posts


@app.post("/posts/", response_model=schemas.Post)
def posts_create(
    user_id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db)
):
    posts = crud.create_post(db, post, user_id)
    return posts
