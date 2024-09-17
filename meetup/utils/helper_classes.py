from uuid import UUID, uuid4
from typing import List, Optional
from datetime import time, date, datetime
from pydantic import BaseModel, HttpUrl, Field, field_serializer


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


class RedisJob(BaseModel):
    job_id: UUID = Field(default_factory=uuid4)
    name: str
    # is_complete: bool = Field(default=False)
    date_published: datetime = Field(default_factory=datetime.now)

    # TODO: Add metadata field

    @field_serializer("date_published", when_used="json")
    def serialize_date_published(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")