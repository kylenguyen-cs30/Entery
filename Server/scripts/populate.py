import sys
import os
from pathlib import Path

# Add the project root directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

from app.database.models import Title, Base
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re

# Create database connection
DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def parse_data_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Split content into sections and clean up
    sections = content.split("_____________________________________________")
    titles = []

    # Parse Games
    games_section = sections[0].split("Games and Developers:")[-1].strip()
    game_entries = re.findall(
        r"\n\n(.*?)\n-(.*?)\n(.*?\.png)", games_section, re.DOTALL
    )
    for title, developer, image in game_entries:
        if title.strip():
            titles.append(
                {
                    "title_name": title.strip(),
                    "category": "Game",
                    "title_cover": f"games/{image.strip()}",
                }
            )

    # Parse Movies
    movies_section = sections[1].split("Movies and Writer/Director:")[-1].strip()
    movie_entries = re.findall(
        r"\n\n(.*?)\n-(.*?)\n(.*?\.png)", movies_section, re.DOTALL
    )
    for title, director, image in movie_entries:
        if title.strip():
            titles.append(
                {
                    "title_name": title.strip(),
                    "category": "Movie",
                    "title_cover": f"movies/{image.strip()}",
                }
            )

    # Parse TV Shows
    tv_section = sections[2].split("TV and Creators:")[-1].strip()
    tv_entries = re.findall(r"\n\n(.*?)\n-(.*?)\n(.*?\.png)", tv_section, re.DOTALL)
    for title, creator, image in tv_entries:
        if title.strip():
            titles.append(
                {
                    "title_name": title.strip(),
                    "category": "TVShow",
                    "title_cover": f"tv/{image.strip()}",
                }
            )

    # Parse Books
    books_section = sections[3].split("Books:")[-1].strip()
    book_entries = re.findall(
        r"\n\n(.*?)\n-(.*?)\n(.*?\.png)", books_section, re.DOTALL
    )
    for title, author, image in book_entries:
        if title.strip():
            titles.append(
                {
                    "title_name": title.strip(),
                    "category": "Book",
                    "title_cover": f"books/{image.strip()}",
                }
            )

    return titles


def populate_database():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create database session
    db = SessionLocal()

    try:
        # Clear existing data
        db.query(Title).delete()

        # Parse data file
        titles = parse_data_file(os.path.join(script_dir, "data.txt"))

        # Add titles to database
        for title_data in titles:
            title = Title(
                title_name=title_data["title_name"],
                category=title_data["category"],
                title_cover=title_data["title_cover"],
            )
            db.add(title)

        # Commit changes
        db.commit()
        print(f"Successfully populated database with {len(titles)} titles")

    except Exception as e:
        print(f"Error populating database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    populate_database()
