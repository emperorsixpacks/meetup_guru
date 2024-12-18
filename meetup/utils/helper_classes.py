from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime, time
from enum import StrEnum
from typing import Dict, List, Optional
from urllib.parse import urlencode, urlunparse
from uuid import UUID, uuid4

import pika
from meetup.utils.global_settings import RabbitMQSettings
from meetup.utils.helper_functions import format_date, formate_time
from pydantic import (BaseModel, ConfigDict, Field, HttpUrl, field_serializer,
                      model_serializer)
from retry import retry


class JOB_STATE(StrEnum):
    SCRAPPER = "srapper_job"
    EMAIL = "email_job"
    COMPLETED = "completed"


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

    @model_serializer()
    def serialize_event(self):
        return {
            "start_date": format_date(self.start_date),
            "end_date": formate_time(self.end_time),
            "start_time": formate_time(self.start_time),
            "end_time": self.end_time(self.end_time),
        }


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


class EventBriteSubCategory(
    BaseModel
):  # TODO: change name to accomodate other scrapper
    id: str
    name: str


class ScrapperMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str
    category: EventBriteCategory
    country: str
    city: str
    events: Optional[list[EventBriteEvent]] = None

    # TODO: add validators for country and city


class RedisJob(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    job_id: UUID = Field(default_factory=uuid4)
    name: str
    scrapper_meta_data: ScrapperMetadata
    job_state: JOB_STATE
    is_complete: bool = Field(default=False)
    date_published: datetime = Field(default_factory=datetime.now)

    @field_serializer("date_published", when_used="always")
    def serialize_date_published(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")


class Message(BaseModel):
    text: str
    date_published: datetime = Field(default_factory=datetime.now)

    @field_serializer("date_published", when_used="always")
    def serialize_date_published(self, value: datetime) -> str:

        return value.strftime("%Y-%m-%d %H:%M:%S")


class BaseRabbitMQConsumer(ABC):
    queues: List[str] = None
    settings: RabbitMQSettings = None

    def __init__(self) -> None:
        self.connection = None
        self.channel = None

    def __init_subclass__(cls) -> None:
        if cls.queues is None:
            raise ValueError("Provide list of queues")
        if cls.settings is None:
            raise ValueError("Provide rabbitmq settings")

    @retry(
        exceptions=pika.exceptions.AMQPConnectionError,
        tries=3,
        delay=1,
        backoff=2,
    )
    def _setup_connection(self) -> None:
        connection_parameters = pika.URLParameters(
            f"amqp://{self.settings.rabbitmq_user}:{self.settings.rabbitmq_password}@{
                self.settings.rabbitmq_host}:{self.settings.rabbitmq_port}/"
        )

        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()

        for queue in self.queues:
            self.channel.queue_declare(queue=queue, durable=True)

    @abstractmethod
    def callback(self, ch, method, properties, body):
        pass

    def consume(self):
        try:
            for queue in self.queues:
                self.channel.basic_consume(
                    queue=queue, on_message_callback=self.callback, auto_ack=True
                )
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

    def publish(self, queue: str, message: Message):
        if queue not in self.queues:
            raise ValueError("Queue not found")
        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=message.model_dump_json(),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def __enter__(self):
        self._setup_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.channel:
            self.channel.close()

        if self.connection:
            self.connection.close()


@dataclass
class URL:
    scheme: str
    path: str
    qparams: Dict[str, str]

    def construct_url(self):
        query_string = urlencode(self.qparams, doseq=True)
        url = urlunparse((self.scheme, self.path, "", "", query_string, ""))
        return url
