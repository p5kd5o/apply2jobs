from logging import getLogger
from typing import Sequence

import models
import sites
import storage

from services.base_service import _BaseService

LOGGER = getLogger(__name__)


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
        results = []
        try:
            searcher = sites.SEARCH_SUPPORTED[site.host](
                self.__clients[site.host]
            )
        except KeyError:
            LOGGER.warning(
                "No ``search'' support for site: %s",
                site.host
            )
        else:
            for job_search in site.jobs:
                LOGGER.info(
                    "Search: %s: %s",
                    site.host,
                    job_search.model_dump_json()
                )
                try:
                    jobs = searcher(**job_search.model_dump())
                except Exception as exc:
                    LOGGER.warning("%s", exc)
                else:
                    results.extend(self.backend.create_many(models.Job, *jobs))
        return results
