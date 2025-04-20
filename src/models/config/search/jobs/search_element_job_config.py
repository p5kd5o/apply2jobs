from enum import Enum, StrEnum
from typing import Annotated, Optional

from pydantic import (
    BeforeValidator, SerializationInfo, field_serializer
)

from utils.models import ensure_enum

from models.base_model import _BaseModel


class SearchElementJobExperience(StrEnum):
    INTERNSHIP = "1"
    ENTRY_LEVEL = "2"
    ASSOCIATE = "3"
    MID_SENIOR_LEVEL = "4"
    DIRECTOR = "5"
    EXECUTIVE = "6"


class SearchElementJobType(StrEnum):
    FULLTIME = "F"
    PARTTIME = "P"
    CONTRACT = "C"
    TEMPORARY = "T"
    INTERNSHIP = "I"
    VOLUNTEER = "V"
    OTHER = "O"


class SearchElementJobRemote(StrEnum):
    ONSITE = "1"
    REMOTE = "2"
    HYBRID = "3"


# pylint: disable=too-few-public-methods
class SearchElementJobConfig(_BaseModel):
    keywords: Optional[str] = None
    experience: Optional[list[Annotated[
        SearchElementJobExperience,
        BeforeValidator(ensure_enum(SearchElementJobExperience))
    ]]] = []
    job_type: Optional[list[Annotated[
        SearchElementJobType,
        BeforeValidator(ensure_enum(SearchElementJobType))
    ]]] = []
    remote: Optional[list[Annotated[
        SearchElementJobRemote,
        BeforeValidator(ensure_enum(SearchElementJobRemote))
    ]]] = []
    location_name: Optional[str] = None
    distance: Optional[int] = None

    @field_serializer("experience", "job_type", "remote")
    def _serialize_enum_list(
        self, field_value: list[Enum], _: SerializationInfo
    ) -> list[str]:
        return [element.value for element in field_value]
