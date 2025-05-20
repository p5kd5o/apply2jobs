from logging import getLogger
from typing import Iterator

from models import Config

from services.base_service import _BaseService

LOGGER = getLogger(__name__)


class ConfigService(_BaseService):

    def find_config(self, **constraints) -> Iterator[Config]:
        return self.backend.find(Config, constraints)
