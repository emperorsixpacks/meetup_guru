import asyncio

from meetup.utils.session_manager import Session
from meetup.utils.global_settings import RabbitMQSettings, RedisSettings
from meetup.utils.helper_classes import (
    BaseRabbitMQConsumer,
    Message,
    JOB_STATE,
    RedisJob,
)
from meetup.utils.helper_functions import is_valid_uuid, flatten_events
from meetup.utils.redis import RedisClient

from meetup.scrapper.scrappers import EventBiteScrapper

rabbitmq_settings = RabbitMQSettings()
redis_settings = RedisSettings()
redis_client = RedisClient(redis_settings)


class Scrapper(BaseRabbitMQConsumer):
    queues = ["scrapper_queue"]
    settings = rabbitmq_settings

    async def process_with_event_brite_scrapper(self, job: RedisJob):
        async with Session() as session:
            event_brite_scrapper = EventBiteScrapper(
                session=session, category=job.scrapper_meta_data.category, city=job.scrapper_meta_data.city, country=job.scrapper_meta_data.city
            ).search()
            return await self.process(event_brite_scrapper)

    def callback(self, ch, method, properties, body):
        print("I see you")
        message = Message.model_validate_json(body.decode("utf-8"))
        if not is_valid_uuid(message.text):
            # TODO add a logger here
            return None
        job = redis_client.get_job(message.text)
        if job is None:
            # TODO add a logger here
            return None
        if job.job_state != JOB_STATE.SCRAPPER:
            # TODO add a logger here
            return None

        try:
            running_loop = asyncio.get_event_loop()
        except RuntimeError:  # For cases where no event loop exists
            running_loop = asyncio.new_event_loop()  # TODO deprecated replace
            asyncio.set_event_loop(running_loop)  # TODO deprecated replace
        running_loop.run_until_complete(self.process_with_event_brite_scrapper(job=job))

        return None

    async def process(self, scrapper):

        tasks = [scrapper.ascrape(page) for page in range(scrapper.total_pages + 1)]
        response = await asyncio.gather(*tasks)

        return flatten_events(response)


class main:
    with Scrapper() as scrapper:
        scrapper.consume()


if __name__ == "__main__":
    main()
