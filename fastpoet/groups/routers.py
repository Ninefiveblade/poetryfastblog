"""Routing module for groups."""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastpoet.settings.database import engine, get_db

from .models import Group
from .schemas import GroupCreate, GroupList
from .service import create_group, get_groups

router = APIRouter()

Group.metadata.create_all(bind=engine)


@router.get("/groups/", response_model=List[GroupList])
def group_get(db: Session = Depends(get_db)) -> Group:
    """Get grous."""
    groups = get_groups(db)
    return groups


@router.post("/groups/", response_model=GroupCreate)
def group_create(group: GroupCreate, db: Session = Depends(get_db)) -> Group:
    """Create new group."""
    group = create_group(db, group)
    return group
