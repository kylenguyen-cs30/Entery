from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional
from sqlalchemy import Enum

import enum


class CategoryType(str, enum.Enum):
    GAME = "Game"
    MOVIE = "Movie"
    TVSHOW = "TVShow"
    BOOK = "Book"


class TitleBase(BaseModel):
    title_name: str
    category: CategoryType
    title_cover: str
    date_started: Optional[date] = None
    date_ended: Optional[date] = None
    complete_counter: int = 0

    model_config = ConfigDict(from_attributes=True)


class TitleCreate(TitleBase):
    pass


class Title(TitleBase):
    title_cover: str
    title_id: int

    class Config:
        from_attribute = True

    @property
    def title_cover_url(self) -> str:
        return f"/images/{self.title_cover}"


class UserTitleBase(BaseModel):
    user_title_name: str
    category: CategoryType
    user_title_cover: str
    date_started: Optional[date] = None
    date_ended: Optional[date] = None
    complete_counter: int = 0


class UserTitleCreate(UserTitleBase):
    pass


class UserTitle(UserTitleBase):
    user_title_id: int

    class Config:
        from_attributes = True


class TrackingStatus(str, Enum):
    ACTIVE = "active"
    STOPPED = "stopped"
    FINISHED = "finished"


class TrackingBase(BaseModel):
    title_id: int
    status: str = "active"

    model_config = ConfigDict(from_attribute=True)


class Tracking(BaseModel):
    tracking_id: int
    title_id: int
    date_started: datetime
    date_ended: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}


class TrackingCreate(BaseModel):
    title_id: int
    status: str = "active"


class TrackingUpdate(BaseModel):
    status: str
    date_ended: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
