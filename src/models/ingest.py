from enum import StrEnum
from typing import Optional

from pydantic import AwareDatetime, NonNegativeInt

from .base_model import _BaseModel


class IngestStatus(StrEnum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    FAILED = "Failed"
    COMPLETED = "Completed"


# pylint: disable=too-few-public-methods
class Ingest(_BaseModel):
    status: IngestStatus
    scheduled_time: Optional[AwareDatetime] = None
    started_time: Optional[AwareDatetime] = None
    stopped_time: Optional[AwareDatetime] = None
    n_processed: Optional[NonNegativeInt] = None
    errors: Optional[list[str]] = None
    site: Optional[str] = None
