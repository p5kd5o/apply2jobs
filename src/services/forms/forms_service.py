from logging import getLogger
from typing import Iterable, Iterator
from urllib.parse import urlparse

from models import Form, Job
from sites import EXTRACT_SUPPORTED
from utils.types import _Id

from services.base_service import _BaseService

LOGGER = getLogger(__name__)


class FormsService(_BaseService):

    def find_forms(self, **constraints) -> Iterator[Form]:
        return self.backend.find(Form, constraints)

    def extract_one(self, job: Job) -> _Id | None:
        form = self._extract_one_form(job)
        if form is None:
            return None
        return self.backend.create(form).created_id

    def extract_many(self, *jobs: Job) -> list[_Id]:
        return self.backend.create_many(
            Form, *self._extract_many_forms(jobs)
        ).created_ids

    def _extract_many_forms(
        self,
        jobs: Iterable[Job]
    ) -> list[Form]:
        return [
            form for form in map(self._extract_one_form, jobs)
            if form is not None
        ]

    def _extract_one_form(
        self,
        job: Job
    ) -> Form | None:
        site_hostname = urlparse(job.apply_url).hostname
        try:
            extractor_type = EXTRACT_SUPPORTED[site_hostname]
        except KeyError:
            LOGGER.warning(
                "no ``extract'' support for site: %s",
                site_hostname
            )
            return None
        try:
            extractor = extractor_type()
            return extractor.main(job)
        except Exception as exc:
            LOGGER.warning(
                "error: %s: %s",
                site_hostname,
                exc
            )
            return None
