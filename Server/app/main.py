from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import titles, tracking, images
from app.database.models import Base
from app.database.connection import engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Entertainment Tracker API")

app.mount("/images", StaticFiles(directory="app/images"), name="images")


app.include_router(titles.router)
app.include_router(tracking.router)
app.include_router(images.router)


@app.get("/")
async def root():
    """
    Root endpoint that redirects to documentation
    """
    return {
        "message": "Welcome to Entertainment Tracker API",
        "documentation": "/docs",
        "health_check": "/health",
    }
