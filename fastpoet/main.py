"""Тестирование"""
from enum import Enum
from typing import Optional, List

from fastapi import FastAPI, Query
from pydantic import BaseModel


class Item(BaseModel):
    title: str
    group: str
    author: int
    text: Optional[str] = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_items(
    q: Optional[List[int]] = Query(None)
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/")
async def index(skip: int = 0, limit: int = 10):
    return db[skip: skip + limit]


@app.get("/{post_id}/")
async def post(post_id: int):
    return {"post_id": post_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/posters/{item_id}")
async def read_item(
    item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": (
                    "This is an amazing item that has a long description"
                )
            }
        )
    return item


@app.post("/posts/")
def post_create(item: Item):
    print(item.dict())
    return item
