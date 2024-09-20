from uuid import UUID, uuid4
from typing import List, Optional, Dict
from datetime import time, date, datetime
from abc import ABC, abstractmethod
from enum import StrEnum
from dataclasses import dataclass
from urllib.parse import urlencode, urlparse, urlunparse

import pika
from retry import retry
from pydantic import BaseModel, HttpUrl, Field, field_serializer, ConfigDict
from meetup.utils.global_settings import RabbitMQSettings


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


class EventBriteSubCategory(BaseModel):  # TODO: change name to accomodate other scrapper
    id: str
    name: str


class ScrapperMetadata(BaseModel):
    name: str
    category: EventBriteCategory
    country: str
    city: str

    # TODO: add validators for country and city


class RedisJob(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    job_id: UUID = Field(default_factory=uuid4)
    name: str
    scrapper_meta_data: ScrapperMetadata
    job_state: JOB_STATE
    is_complete: bool = Field(default=False)
    date_published: datetime = Field(default_factory=datetime.now)

    @field_serializer("date_published", when_used="json")
    def serialize_date_published(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")


class Message(BaseModel):
    text: str
    date_published: datetime = Field(default_factory=datetime.now)

    @field_serializer("date_published", when_used="json")
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
            f"amqp://{self.settings.rabbitmq_user}:{self.settings.rabbitmq_password}@{self.settings.rabbitmq_host}:{self.settings.rabbitmq_port}/"
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
