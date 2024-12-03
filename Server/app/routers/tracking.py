from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database.connection import SessionLocal
from app.database import models
from app.models import schemas
from app.dependencies import get_db

router = APIRouter(prefix="/tracking", tags=["tracking"])


@router.post("/", response_model=schemas.Tracking)
def create_tracking(tracking: schemas.TrackingCreate, db: Session = Depends(get_db)):
    # Check if title exists
    db_title = (
        db.query(models.Title)
        .filter(models.Title.title_id == tracking.title_id)
        .first()
    )
    if not db_title:
        raise HTTPException(status_code=404, detail="Title not found")

    # Check if already tracking
    existing_tracking = (
        db.query(models.Tracking)
        .filter(
            models.Tracking.title_id == tracking.title_id,
            models.Tracking.status == "active",  # Changed from enum to string
        )
        .first()
    )
    if existing_tracking:
        raise HTTPException(status_code=400, detail="Title is already being tracked")

    # Create new tracking
    db_tracking = models.Tracking(
        title_id=tracking.title_id,
        status="active",  # Default to active string
        date_started=datetime.now(),
    )
    db.add(db_tracking)
    db.commit()
    db.refresh(db_tracking)
    return db_tracking


@router.put("/{tracking_id}", response_model=schemas.Tracking)
def update_tracking(
    tracking_id: int,
    tracking_update: schemas.TrackingUpdate,
    db: Session = Depends(get_db),
):
    db_tracking = (
        db.query(models.Tracking)
        .filter(models.Tracking.tracking_id == tracking_id)
        .first()
    )
    if not db_tracking:
        raise HTTPException(status_code=404, detail="Tracking not found")

    # Update status directly as string
    db_tracking.status = tracking_update.status

    # If status is finished, set end date
    if tracking_update.status == "finished":
        db_tracking.date_ended = datetime.now()
    elif tracking_update.date_ended:
        db_tracking.date_ended = tracking_update.date_ended

    db.commit()
    db.refresh(db_tracking)
    return db_tracking


@router.get("/", response_model=List[schemas.Tracking])
def get_all_tracking(db: Session = Depends(get_db)):
    return db.query(models.Tracking).all()
