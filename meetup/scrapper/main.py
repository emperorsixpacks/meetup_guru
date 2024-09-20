import asyncio

from meetup.utils.session_manager import Session
from meetup.utils.global_settings import RabbitMQSettings, RedisSettings
from meetup.utils.helper_classes import BaseRabbitMQConsumer, Message, JOB_STATE
from meetup.utils.helper_functions import is_valid_uuid
from meetup.utils.redis import RedisClient

from meetup.scrapper.scrappers import EventBiteScrapper

rabbitmq_settings = RabbitMQSettings()
redis_settings = RedisSettings()
redis_client = RedisClient(redis_settings)


class Scrapper(BaseRabbitMQConsumer):
    queues = ["scrapper_queue"]
    settings = rabbitmq_settings

    async def process_with_event_brite_scrapper(self):
        async with Session() as session:
            event_brite_scrapper =  EventBiteScrapper(
                session=session,  city="lagos", country="nigeria"
            ).search()
            return await self.process(event_brite_scrapper)
        

    def callback(self, ch, method, properties, body):
        print("I see you")
        pages = []
        # message = Message.model_validate_json(body.decode("utf-8"))
        # if not is_valid_uuid(message.text):
        #     #TODO add a logger here
        #     return 0
        # job = redis_client.get_job(message.text)
        # if job is None:
        #     #TODO add a logger here
        #     return 0
        # if job.job_state != JOB_STATE.SCRAPPER:
        #     #TODO add a logger here
        #     return 0

        try:
            running_loop = asyncio.get_event_loop()
        except RuntimeError:  # For cases where no event loop exists
            running_loop = asyncio.new_event_loop()  #TODO deprecated
            asyncio.set_event_loop(running_loop)  #TODO deprecated
        running_loop.run_until_complete(self.process_with_event_brite_scrapper())

    async def process(self, scrapper):
        print(scrapper.total_pages)
        tasks = [
            scrapper.ascrape(page)
            for page in range(scrapper.total_pages + 1)
        ]
        print(tasks)
        response = await asyncio.gather(*tasks)

        print(response)
        return response


class main:
    with Scrapper() as scrapper:
        scrapper.consume()


if __name__ == "__main__":
    main()
