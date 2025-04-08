from logging import getLogger
from typing import Sequence

import models

from services.base_service import _BaseService

LOGGER = getLogger(__name__)


class JobsService(_BaseService):

    def get_all(self) -> Sequence[models.Job]:
        return self.backend.find(models.Job, {})
