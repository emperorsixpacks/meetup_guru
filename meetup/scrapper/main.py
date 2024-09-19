
from meetup.utils.global_settings import RabbitMQSettings, RedisSettings
from meetup.utils.helper_classes import BaseRabbitMQConsumer
from meetup.utils.redis import RedisClient

rabbitmq_settings = RabbitMQSettings()
redis_settings = RedisSettings()
redis_client = RedisClient(redis_settings)


class Scrapper(BaseRabbitMQConsumer):
    queues = ["scrapper_queue"]
    settings = rabbitmq_settings

    def callback(self, ch, method, properties, body):
        job_id = str(body)
        job = redis_client.get_job(job_id)
        if job is None:
            # TODO add logger here
            print(f"Job with id {job_id} not found")
        
        


class main():
    with Scrapper() as scrapper:
        scrapper.consume()

if __name__ == "__main__":
    main()