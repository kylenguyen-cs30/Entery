from sys import prefix
from app import routers
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import os

router = APIRouter(prefix="/images", tags=["images"])

# Configure your image directory
IMAGES_DIR = Path("app/images")

# Create images directory if it does  not exist
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/{category}/{image_name}")
async def get_image(category: str, image_name: str):
    image_path = IMAGES_DIR / category / image_name
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)
