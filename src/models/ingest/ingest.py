from enum import Enum, StrEnum
from typing import Annotated, Any, Optional

from pydantic import (
    AwareDatetime, BeforeValidator, SerializationInfo,
    field_serializer
)

from models.base_model import _BaseModel
from utils.enums import ensure_enum
from utils.types import _Id


class IngestStatus(StrEnum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    FAILED = "Failed"
    CANCELED = "Canceled"
    COMPLETED = "Completed"


# pylint: disable=too-few-public-methods
class Ingest(_BaseModel):
    status: Annotated[IngestStatus, BeforeValidator(ensure_enum(IngestStatus))]
    scheduled_time: Optional[AwareDatetime] = None
    started_time: Optional[AwareDatetime] = None
    stopped_time: Optional[AwareDatetime] = None
    job_ids: Optional[list[_Id]] = None
    errors: Optional[list[str]] = None
    site: Optional[str] = None

    @field_serializer("status")
    def _serialize_enum(self, field_value: Enum, _: SerializationInfo) -> Any:
        return field_value.value
