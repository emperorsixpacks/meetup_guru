from typing import List
from datetime import time, date
from pydantic import BaseModel, HttpUrl


class Location(BaseModel):
    logitude: float
    latitude: float

class Event(BaseModel):
    name: str
    url:  HttpUrl
    city: str
    country: str
    summary: str
    # address: str
    # image_url: HttpUrl
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