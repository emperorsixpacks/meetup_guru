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

class ScrapperMetadata(BaseModel):
    name: str
    category: EventBriteCategory
    

class RedisJob(BaseModel):
    job_id: UUID = Field(default_factory=uuid4)
    name: str
    scrapper_meta_data: ScrapperMetadata
    is_complete: bool = Field(default=False)
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

        return None
    
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

    # def publish(self, message):


    def __enter__(self):
        self._setup_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.channel:
            self.channel.close()

        if self.connection:
            self.connection.close()