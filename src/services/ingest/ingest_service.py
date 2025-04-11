from datetime import UTC, datetime, timedelta
from logging import getLogger
from typing import Sequence

import models
import sites
import storage

from services.base_service import _BaseService

LOGGER = getLogger(__name__)

DT_UTC_MIN = datetime(1, 1, 1, 0, 0, 0, tzinfo=UTC)


class IngestService(_BaseService):
    __clients: dict[str, object]

    def __init__(
        self,
        backend: storage._BaseBackend,
        site_config: Sequence[models.SearchElementConfig]
    ):
        super().__init__(backend)
        self.__clients = self._init_search_clients(site_config)

    @staticmethod
    def _init_search_clients(
        site_config: Sequence[models.SearchElementConfig]
    ) -> dict[str, object]:
        search_clients = {}
        for site in site_config:
            search_client_kwgs = {}
            for name, credential in site.auth.credentials:
                search_client_kwgs[name] = credential.value
            search_clients[site.host] = sites.SITE_CLIENT_TYPE[site.host](
                **search_client_kwgs
            )
        return search_clients

    def ingest_all(
        self,
        site_config: Sequence[models.SearchElementConfig]
    ) -> dict[str, list]:
        return {site.host: self.ingest_site(site) for site in site_config}

    def ingest_site(self, site: models.SearchElementConfig) -> list:
        completed_ingests = self.backend.find(
            models.Ingest,
            {
                "site": site.host,
                "status": models.IngestStatus.COMPLETED
            }
        )
        previous_ingest = max(
            completed_ingests,
            key=lambda x:
                x.stopped_time if isinstance(x.stopped_time, datetime)
                else DT_UTC_MIN,
            default=None
        )
        previous_ingest_dt = getattr(
            previous_ingest,
            "stopped_time",
            datetime.now(tz=UTC) - timedelta(days=1)
        )
        ingest = models.Ingest(
            status=models.IngestStatus.PENDING,
            scheduled_time=datetime.now(tz=UTC),
            site=site.host
        )
        ingest_id = self.backend.create(ingest).created_id

        jobs = []
        try:
            searcher_type: type[sites._BaseSearch] = (
                sites.SEARCH_SUPPORTED[site.host]
            )
        except KeyError:
            LOGGER.warning(
                "no ``search'' support for site: %s",
                site.host
            )
            ingest = models.Ingest(
                status=models.IngestStatus.FAILED,
                scheduled_time=ingest.scheduled_time,
                stopped_time=datetime.now(tz=UTC),
                n_processed=0,
                errors=["no ``search'' support for site"],
                site=site.host
            )
            self.backend.update(ingest_id, ingest)
        else:
            ingest = models.Ingest(
                status=models.IngestStatus.IN_PROGRESS,
                scheduled_time=ingest.scheduled_time,
                started_time=datetime.now(tz=UTC),
                site=site.host
            )
            self.backend.update(ingest_id, ingest)
            errors = []
            for job_search in site.jobs:
                LOGGER.info(
                    "search: %s: %s",
                    site.host,
                    job_search.model_dump_json()
                )
                try:
                    searcher = searcher_type(self.__clients[site.host])
                    listed_within = datetime.now(tz=UTC) - previous_ingest_dt
                    search_results = searcher.main(
                        **job_search.model_dump(),
                        listed_at=int(listed_within.total_seconds() // 1)
                    )
                    jobs.extend(search_results)
                except Exception as exc:
                    LOGGER.warning("%s", exc)
                    errors.append(exc)

            ingest = models.Ingest(
                status=models.IngestStatus.COMPLETED,
                scheduled_time=ingest.scheduled_time,
                started_time=ingest.started_time,
                stopped_time=datetime.now(tz=UTC),
                n_processed=len(jobs),
                errors=list(map(str, errors)),
                site=site.host
            )
            self.backend.update(ingest_id, ingest)

        return self.backend.create_many(models.Job, *jobs)
