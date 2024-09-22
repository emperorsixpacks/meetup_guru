import json
from uuid import UUID
from redis import Redis

from meetup.utils.helper_classes import RedisJob, JOB_STATE
from meetup.utils.global_settings import RedisSettings
from meetup.utils.global_errors import FailedToCreateRedisJobError


class RedisClient:
    def __init__(self, settings: RedisSettings):
        self._client = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            db=settings.redis_db,
        )

    def new_job(self, redis_job: RedisJob) -> RedisJob:
        new_job = self._client.set(str(redis_job.job_id), redis_job.model_dump_json())
        if new_job == 0:
            raise FailedToCreateRedisJobError(
                f"Failed to create job with id {redis_job.job_id}"
            )
        return new_job

    def get_job(self, job_id: UUID) -> RedisJob:
        job = self._client.get(str(job_id))
        if job is None:
            return None
            # raise ValueError(f"Job with id {job_id} not found")  # TODO: use a logger here
        job = json.loads(job)
        return RedisJob(**job)

    def update_job(self, job_id: UUID, job: RedisJob) -> RedisJob:
        print(job.model_dump_json())
        updated_job = self._client.set(str(job_id), job.model_dump_json()) # TODO: look into hset again
        if updated_job == 0:
            return None  # TODO: add custom exception

        return job

    def delete_job(self, job_id: UUID) -> bool:
        pass

    def get_job_status(self, job_id: UUID) -> bool:
        # TODO: not implemnted, I mean I have not added the update method
        return bool(self.get_job(job_id).is_complete)

    def update_job_state(self, job_id: UUID, state: JOB_STATE) -> bool:
        job = self.get_job(job_id=job_id)
        job.job_state = state
        return self.update_job(job_id, job)
