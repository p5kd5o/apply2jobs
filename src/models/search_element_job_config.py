from enum import Enum
from typing import Annotated, Optional

from pydantic import (
    BeforeValidator, SerializationInfo, field_serializer
)

from utils.models import ensure_enum

from .base_model import _BaseModel


class SearchElementJobExperience(str, Enum):
    INTERNSHIP = "1"
    ENTRY_LEVEL = "2"
    ASSOCIATE = "3"
    MID_SENIOR_LEVEL = "4"
    DIRECTOR = "5"
    EXECUTIVE = "6"


class SearchElementJobType(str, Enum):
    FULLTIME = "F"
    PARTTIME = "P"
    CONTRACT = "C"
    TEMPORARY = "T"
    INTERNSHIP = "I"
    VOLUNTEER = "V"
    OTHER = "O"


class SearchElementJobRemote(str, Enum):
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

    @field_serializer("experience")
    def _serialize_experience(
        self,
        experience: SearchElementJobExperience,
        _: SerializationInfo
    ) -> list[str]:
        return [e.name for e in experience]

    @field_serializer("job_type")
    def _serialize_job_type(
        self,
        job_type: SearchElementJobType,
        _: SerializationInfo
    ) -> list[str]:
        return [e.name for e in job_type]

    @field_serializer("remote")
    def _serialize_remote(
        self,
        remote: SearchElementJobRemote,
        _: SerializationInfo
    ) -> list[str]:
        return [e.name for e in remote]
