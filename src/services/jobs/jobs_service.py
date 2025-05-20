from logging import getLogger
from typing import Iterator

from models import Job

from services.base_service import _BaseService

LOGGER = getLogger(__name__)


class JobsService(_BaseService):

    def find_jobs(self, **constraints) -> Iterator[Job]:
        return self.backend.find(Job, constraints)
