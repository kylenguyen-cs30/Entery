from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import SessionLocal
from app.database import models
from app.models import schemas

router = APIRouter(prefix="/user-titles", tags=["user-titles"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.UserTitle)
def create_user_title(
    user_title: schemas.UserTitleCreate, db: Session = Depends(get_db)
):
    db_user_title = models.UserTitle(**user_title.dict())
    db.add(db_user_title)
    db.commit()
    db.refresh(db_user_title)
    return db_user_title


@router.get("/", response_model=List[schemas.UserTitle])
def read_user_titles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_titles = db.query(models.UserTitle).offset(skip).limit(limit).all()
    return user_titles


@router.get("/{user_title_id}", response_model=schemas.UserTitle)
def read_user_title(user_title_id: int, db: Session = Depends(get_db)):
    db_user_title = (
        db.query(models.UserTitle)
        .filter(models.UserTitle.user_title_id == user_title_id)
        .first()
    )
    if db_user_title is None:
        raise HTTPException(status_code=404, detail="User Title not found")
    return db_user_title


@router.put("/{user_title_id}", response_model=schemas.UserTitle)
def update_user_title(
    user_title_id: int,
    user_title: schemas.UserTitleCreate,
    db: Session = Depends(get_db),
):
    db_user_title = (
        db.query(models.UserTitle)
        .filter(models.UserTitle.user_title_id == user_title_id)
        .first()
    )
    if db_user_title is None:
        raise HTTPException(status_code=404, detail="User Title not found")

    for key, value in user_title.dict().items():
        setattr(db_user_title, key, value)

    db.commit()
    db.refresh(db_user_title)
    return db_user_title
