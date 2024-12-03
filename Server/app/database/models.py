from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from .connection import Base
import enum


class Title(Base):
    __tablename__ = "titles"

    title_id = Column(Integer, primary_key=True, index=True)
    title_name = Column(String, index=True)
    category = Column(
        Enum("Game", "Movie", "TVShow", "Book", name="category_types"), nullable=False
    )
    title_cover = Column(String)  # URL for image
    date_started = Column(Date, nullable=True)
    date_ended = Column(Date, nullable=True)
    complete_counter = Column(Integer, default=0)

    # Relationship with user collections
    user_collections = relationship("UserCollection", back_populates="title")

    @property
    def title_cover_url(self):
        # self.category
        category_folder = {
            "Game": "games",
            "Movie": "movies",
            "TVShow": "tv",
            "Book": "books",
        }
        folder = category_folder.get(self.category, "")
        # return the full URL when needed
        return f"{folder}/{self.title_cover}"


class UserTitle(Base):
    __tablename__ = "user_titles"

    user_title_id = Column(Integer, primary_key=True, index=True)
    user_title_name = Column(String, index=True)
    category = Column(
        Enum("Game", "Movie", "TVShow", "Book", name="category_types"), nullable=False
    )
    user_title_cover = Column(String)  # URL for image
    date_started = Column(Date, nullable=True)
    date_ended = Column(Date, nullable=True)
    complete_counter = Column(Integer, default=0)

    # Relationship with user collections
    user_collections = relationship("UserCollection", back_populates="user_title")


class UserCollection(Base):
    __tablename__ = "user_collections"

    id = Column(Integer, primary_key=True, index=True)
    title_id = Column(Integer, ForeignKey("titles.title_id"), nullable=True)
    user_title_id = Column(
        Integer, ForeignKey("user_titles.user_title_id"), nullable=True
    )

    # Relationships
    title = relationship("Title", back_populates="user_collections")
    user_title = relationship("UserTitle", back_populates="user_collections")


class TrackingStatus(str, enum.Enum):
    ACTIVE = "active"
    STOPPED = "stopped"
    FINISHED = "finished"


class Tracking(Base):
    __tablename__ = "tracking"

    tracking_id = Column(Integer, primary_key=True, index=True)
    title_id = Column(Integer, ForeignKey("titles.title_id"))
    date_started = Column(DateTime, server_default=func.now())
    date_ended = Column(DateTime, nullable=True)
    status = Column(String, default="active")

    def to_dict(self):
        return {
            "tracking_id": self.tracking_id,
            "title_id": self.title_id,
            "date_started": self.date_started,
            "date_ended": self.date_ended,
            "status": self.status,
        }
