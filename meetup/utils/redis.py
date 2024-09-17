from uuid import UUID
from typing import Optional
from redis import Redis

from meetup.utils.helper_classes import RedisJob
from meetup.utils.global_settings import RedisSettings
from meetup.utils.global_errors import FailedToCreateRedisJobError

class RedisClient(Redis):
    def __init__(self, settings:RedisSettings):
        super().__init__(host=settings.redis_host, port=settings.redis_port, password=settings.redis_password, db=settings.redis_db)
    
    def new_job(self, job: RedisJob) -> RedisJob:
        new_job = self.set(str(job.job_id), job.model_dump_json())
        if new_job == 0:
            raise FailedToCreateRedisJobError(f"Failed to create job with id {job.job_id}")
        return new_job

    def get_job(self, job_id: UUID) -> RedisJob:
        pass

    def delete_job(self, job_id: UUID) -> bool:
        pass    

    def get_job_status(self, job_id: UUID) -> bool:
        pass

    def update_job_status(self, job_id: UUID, status: bool) -> bool:
        pass



job = RedisJob(name="MY JOB")


RedisClient(settings=RedisSettings()).new_job(job=job)