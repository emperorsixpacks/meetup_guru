from typing import List, Optional
from datetime import time, date
from pydantic import BaseModel, HttpUrl


class Location(BaseModel):
    logitude: float
    latitude: float


class Event(BaseModel):
    name: str
    url: HttpUrl
    city: str
    country: str
    summary: str
    # address: str
    image_url: Optional[HttpUrl] = None
    is_online_event: bool


class EventBriteEvent(Event):
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    # location: Location
    # tags: List[str]


# class Pagination(BaseModel):
#     page: int
#     total_pages: int
#     # events: List[EventBriteEvent]


class EventBriteCategory(BaseModel):
    name: str
    id: int
    name_localized: str
    short_name: str
    short_name_localized: str


class EventBriteSubCategory(BaseModel):
    id: str
    name: str
