# app/routers/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict
from app.database.connection import SessionLocal

router = APIRouter(prefix="/health", tags=["health"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=Dict[str, str])
async def health_check():
    """
    Basic health check endpoint that always returns OK if the server is running
    """
    return {"status": "OK", "message": "Server is running"}


@router.get("/database", response_model=Dict[str, str])
async def database_health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint that verifies database connection
    """
    try:
        # Execute a simple query to check database connection
        db.execute(text("SELECT 1"))
        return {"status": "OK", "message": "Database connection successful"}
    except Exception as e:
        return {"status": "ERROR", "message": f"Database connection failed: {str(e)}"}
