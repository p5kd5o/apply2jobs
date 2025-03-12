from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field

from . import ensure_enum


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
class SearchElementJobConfig(BaseModel, extra="forbid"):
    keywords: Optional[str]
    experience: Optional[list[Annotated[
        SearchElementJobExperience,
        BeforeValidator(ensure_enum(SearchElementJobExperience))
    ]]]
    job_type: Optional[list[Annotated[
        SearchElementJobType,
        BeforeValidator(ensure_enum(SearchElementJobType))
    ]]]
    remote: Optional[list[Annotated[
        SearchElementJobRemote,
        BeforeValidator(ensure_enum(SearchElementJobRemote))
    ]]]
    location_name: Optional[str]
    distance: Optional[int] = None
    limit: Optional[Annotated[int, Field(ge=-1)]]

    def to_dict(self):
        return {
            "keywords": self.keywords,
            "experience": list(map(lambda x: x.value, self.experience)),
            "job_type": list(map(lambda x: x.value, self.job_type)),
            "remote": list(map(lambda x: x.value, self.remote)),
            "location_name": self.location_name,
            "distance": self.distance,
            "limit": self.limit
        }
