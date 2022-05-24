"""Schemas module for posts"""
from pydantic import BaseModel, validator, Field
from typing import List
from .validators import check_name, check_slug, check_year

##### Categories ######
class Categories(BaseModel):
    name: str
    slug: str

    # validators
    _check_name = validator(
        'name', allow_reuse=True, pre=True, always=True
    )(check_name)
    _check_slug = validator(
        'slug', allow_reuse=True, pre=True, always=True
    )(check_slug)

    class Config:
        orm_mode = True


class CategoriesList(Categories):
    id: int


class CategoriesCreate(Categories):
    pass

##### Genres ######
class Genres(BaseModel):
    name: str
    slug: str

    # validators
    _check_name = validator(
        'name', allow_reuse=True, pre=True, always=True
    )(check_name)
    _check_slug = validator(
        'slug', allow_reuse=True, pre=True, always=True
    )(check_slug)

    class Config:
        orm_mode = True


class GenresList(Categories):
    id: int


class GenresCreate(Categories):
    pass

##### Titles ######
class Titles(BaseModel):
    name: str
    year: int
    description: str
    category_id: int
    genre_id: List[int]

    # validators
    _check_year = validator(
        'year', allow_reuse=True, pre=True, always=True
    )(check_year)
    _check_slug = validator(
        'name', allow_reuse=True
    )(check_slug)

    class Config:
        orm_mode = True


class TitlesList(Titles):
    id: int


class TitlesCreate(Titles):
    pass
