from uuid import UUID
from redis import Redis

from meetup.utils.helper_classes import RedisJob
from meetup.utils.global_settings import RedisSettings
from meetup.utils.global_errors import FailedToCreateRedisJobError

class RedisClient:
    def __init__(self, settings:RedisSettings):
        self._client = Redis(host=settings.redis_host, port=settings.redis_port, password=settings.redis_password, db=settings.redis_db)
    
    def new_job(self, redis_job: RedisJob) -> RedisJob:
        new_job = self._client.set(str(redis_job.job_id), redis_job.model_dump_json())
        if new_job == 0:
            raise FailedToCreateRedisJobError(f"Failed to create job with id {job.job_id}")
        return new_job

    def get_job(self, job_id: UUID) -> RedisJob:
        job = self._client.get(str(job_id))
        if job is None:
            return None
            # raise ValueError(f"Job with id {job_id} not found")  # TODO: use a logger here
        return RedisJob.from_json(job)

    def delete_job(self, job_id: UUID) -> bool:
        pass    

    def get_job_status(self, job_id: UUID) -> bool:
        return bool(self.get_job(job_id)["status"])

    def update_job_status(self, job_id: UUID, status: bool) -> bool:
        pass


