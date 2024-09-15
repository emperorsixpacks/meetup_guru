from typing import List
from datetime import datetime
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
    address: str
    image_url: HttpUrl
    is_online_event: bool


class EventBriteEvent(Event):
    start_date: datetime
    end_date: datetime
    start_time: datetime
    end_time: datetime
    location: Location
    tags: List[str]

