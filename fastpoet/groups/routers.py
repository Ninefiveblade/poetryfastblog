"""Routing module for groups."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastpoet.settings.database import engine, get_db

from .models import Group
from .schemas import GroupCreate, GroupList
from .service import get_groups, create_group


router = APIRouter()

Group.metadata.create_all(bind=engine)


@router.get("/groups/", response_model=list[GroupList])
def group_get(db: Session = Depends(get_db)):
    groups = get_groups(db)
    return groups


@router.post("/groups/", response_model=GroupCreate)
def group_create(group: GroupCreate, db: Session = Depends(get_db)):
    """Create new group."""
    group = create_group(db, group)
    return group

