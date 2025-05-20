from datetime import UTC, datetime, timedelta
from logging import getLogger
from typing import Iterable, Iterator

from models import Ingest, IngestStatus, Job, SearchElementConfig
from sites import SEARCH_SUPPORTED, SITE_CLIENT_TYPE
from storage import _BaseBackend
from utils.types import _Id

from services.base_service import _BaseService

LOGGER = getLogger(__name__)

DT_UTC_MIN = datetime(1, 1, 1, 0, 0, 0, tzinfo=UTC)

DEFAULT_LISTED_WITHIN = int(timedelta(days=1).total_seconds())


class IngestService(_BaseService):
    __clients: dict[str, object]

    def __init__(
        self,
        backend: _BaseBackend,
        *site_config: SearchElementConfig
    ):
        super().__init__(backend)
        self.__clients = self._init_search_clients(site_config)

    @staticmethod
    def _init_search_clients(
        site_config: Iterable[SearchElementConfig]
    ) -> dict[str, object]:
        search_clients = {}
        for site in site_config:
            search_client_kwgs = {}
            for name, credential in site.auth.credentials:
                search_client_kwgs[name] = credential.value
            search_clients[site.host] = SITE_CLIENT_TYPE[site.host](
                **search_client_kwgs
            )
        return search_clients

    def find_ingests(self, **constraints) -> Iterator[Ingest]:
        return self.backend.find(Ingest, constraints)

    def ingest_many(self, *sites: SearchElementConfig) -> list[_Id]:
        return list(map(self.ingest_one, sites))

    def ingest_one(self, site: SearchElementConfig) -> _Id:
        ingest = Ingest(
            status=IngestStatus.PENDING,
            scheduled_time=datetime.now(tz=UTC),
            site=site.host
        )
        ingest_id = self.backend.create(ingest).created_id

        try:
            searcher_type = SEARCH_SUPPORTED[site.host]
        except KeyError:
            LOGGER.warning(
                "no ``search'' support for site: %s",
                site.host
            )
            ingest = Ingest(
                status=IngestStatus.FAILED,
                scheduled_time=ingest.scheduled_time,
                stopped_time=datetime.now(tz=UTC),
                job_ids=[],
                errors=["no ``search'' support for site"],
                site=site.host
            )
            self.backend.update(ingest_id, ingest)
            return ingest_id

        try:
            jobs = []
            errors = []
            previous_ingest = self._find_latest_completed(site.host)
            previous_ingest_dt = getattr(previous_ingest, "stopped_time", None)

            ingest = Ingest(
                status=IngestStatus.IN_PROGRESS,
                scheduled_time=ingest.scheduled_time,
                started_time=datetime.now(tz=UTC),
                site=site.host
            )
            self.backend.update(ingest_id, ingest)

            for job_search in site.jobs:
                LOGGER.info(
                    "search: %s: %s",
                    site.host,
                    job_search.model_dump_json()
                )
                try:
                    searcher = searcher_type(self.__clients[site.host])
                    if previous_ingest_dt is None:
                        listed_within = DEFAULT_LISTED_WITHIN
                    else:
                        listed_within = int((
                            datetime.now(tz=UTC) - previous_ingest_dt
                        ).total_seconds())
                    jobs.extend(searcher.main(
                        **job_search.model_dump(), listed_at=listed_within
                    ))
                except Exception as exc:
                    LOGGER.warning("%s", exc)
                    errors.append(exc)

            result = self.backend.create_many(Job, *jobs)
            ingest = Ingest(
                status=IngestStatus.COMPLETED,
                scheduled_time=ingest.scheduled_time,
                started_time=ingest.started_time,
                stopped_time=datetime.now(tz=UTC),
                job_ids=result.created_ids,
                errors=list(map(str, errors)),
                site=site.host
            )
            self.backend.update(ingest_id, ingest)
            return ingest_id

        except Exception as exc:
            LOGGER.warning(
                "ingest cancelled for site: %s: %s",
                site.host,
                exc
            )
            ingest = Ingest(
                status=IngestStatus.CANCELED,
                scheduled_time=ingest.scheduled_time,
                started_time=ingest.started_time,
                stopped_time=datetime.now(tz=UTC),
                job_ids=[],
                errors=[exc],
                site=site.host
            )
            self.backend.update(ingest_id, ingest)
            return ingest_id

    def _find_latest_completed(self, site_host: str) -> datetime | None:
        try:
            latest = max(
                self.backend.find(
                    Ingest,
                    {
                        "site": site_host,
                        "status": IngestStatus.COMPLETED
                    }
                ),
                key=lambda x:
                    x.stopped_time if
                    x.stopped_time is not None
                    else DT_UTC_MIN,
            )
            return latest if latest.stopped_time is not None else None
        except ValueError:
            return None
