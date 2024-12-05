from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

# from app.database.connection import SessionLocal
from app.database import models
from app.models import schemas
from typing import Literal
from app.dependencies import get_db

router = APIRouter(prefix="/titles", tags=["titles"])


# NOTE: create a new title
@router.post("/", response_model=schemas.Title)
def create_title(title: schemas.TitleCreate, db: Session = Depends(get_db)):
    db_title = models.Title(**title.dict())
    db.add(db_title)
    db.commit()
    db.refresh(db_title)
    return db_title


# NOTE: Return all titles
@router.get("/", response_model=List[schemas.Title])
def read_titles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    titles = db.query(models.Title).offset(skip).limit(limit).all()
    return titles


# NOTE: return a title
@router.get("/{title_id}", response_model=schemas.Title)
def read_title(title_id: int, db: Session = Depends(get_db)):
    db_title = db.query(models.Title).filter(models.Title.title_id == title_id).first()
    if db_title is None:
        raise HTTPException(status_code=404, detail="Title not found")
    return db_title


# NOTE: Update a title
@router.put("/{title_id}", response_model=schemas.Title)
def update_title(
    title_id: int, title: schemas.TitleCreate, db: Session = Depends(get_db)
):
    db_title = db.query(models.Title).filter(models.Title.title_id == title_id).first()
    if db_title is None:
        raise HTTPException(status_code=404, detail="Title not found")

    for key, value in title.dict().items():
        setattr(db_title, key, value)

    db.commit()
    db.refresh(db_title)
    return db_title


# NOTE: return all titles that relating to that category
@router.get("/category/{category}", response_model=List[schemas.Title])
def get_titles_by_category(
    category: Literal["Game", "Movie", "TVShow", "Book"], db: Session = Depends(get_db)
):
    titles = db.query(models.Title).filter(models.Title.category == category).all()
    if not titles:
        return []  # Return empty list if no titles found
    return titles


# NOTE: Alternative approach using query parameter
@router.get("/filter", response_model=List[schemas.Title])
def filter_titles(
    category: Literal["Game", "Movie", "TVShow", "Book"] = Query(
        ..., description="Category type"
    ),
    db: Session = Depends(get_db),
):
    titles = db.query(models.Title).filter(models.Title.category == category).all()
    if not titles:
        return []
    return titles
