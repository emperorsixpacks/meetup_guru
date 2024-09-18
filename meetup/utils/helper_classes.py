from uuid import UUID, uuid4
from typing import List, Optional
from datetime import time, date, datetime
from abc import ABC, abstractmethod

import pika
from retry import retry
from pydantic import BaseModel, HttpUrl, Field, field_serializer
from meetup.utils.global_settings import RabbitMQSettings


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


class BaseRabbitMQConsumer(ABC):
    queues: List[str] = None
    settings: RabbitMQSettings = None

    def __init__(self) -> None:
        self.connection  = None
        self.channel = None
        self._setup_connection()

    @retry(
        exceptions=pika.exceptions.AMQPConnectionError,
        tries=3,
        delay=1,
        backoff=2,
    )
    def _setup_connection(self):
        connection_parameters = pika.URLParameters(
            f"amqp://{self.settings.rabbitmq_user}:{self.settings.rabbitmq_password}@{self.settings.rabbitmq_host}:{self.settings.rabbitmq_port}/"
        )

        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()

    def __init_subclass__(cls) -> None:
        if cls.queues is None:
            raise ValueError("Provide list of queues")
        if cls.settings is None:
            raise ValueError("Provide rabbitmq settings")

    @abstractmethod
    def consume(self):
        pass

    @abstractmethod
    def callback(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self):
        pass
