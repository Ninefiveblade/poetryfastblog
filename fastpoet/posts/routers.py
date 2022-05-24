"""Routing module for posts"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastpoet.settings.database import engine, get_db

from .models import Category, Genre
from .schemas import (
    CategoriesCreate, CategoriesList, GenresCreate,
    GenresList, TitlesList, TitlesCreate
)
from .service import (
    get_categories, create_categories, get_genres, 
    create_genres, get_titles, create_titles
)


router = APIRouter()

Category.metadata.create_all(bind=engine)


@router.get("/categories/", response_model=list[CategoriesList])
def categories_get(db: Session = Depends(get_db)):
    categories = get_categories(db)
    return categories


@router.post("/categories/", response_model=CategoriesCreate)
def categories_create(category: CategoriesCreate, db: Session = Depends(get_db)):
    """Create new category"""
    category = create_categories(db, category)
    return category

##### Genres ######

@router.get("/genres/", response_model=list[GenresList])
def genres_get(db: Session = Depends(get_db)):
    genres = get_genres(db)
    return genres

@router.post("/genres/", response_model=GenresCreate)
def genres_create(genre: GenresCreate, db: Session = Depends(get_db)):
    """Create new category"""
    genre = create_genres(db, genre)
    return genre

##### Titles ######

@router.get("/titles/", response_model=list[TitlesList])
def titles_get(db: Session = Depends(get_db)):
    titles = get_titles(db)
    return titles

@router.post("/titles/", response_model=TitlesCreate)
def titles_create(titles: TitlesCreate, db: Session = Depends(get_db)):
    """Create new category"""
    titles = create_titles(db, titles)
    return titles