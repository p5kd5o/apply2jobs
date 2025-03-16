from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field

from utils.models import ensure_enum


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
    limit: Optional[Annotated[int, Field(ge=-1)]] = -1

    def to_dict(self):
        return {
            "keywords": self.keywords,
            "experience": list(x.value for x in self.experience),
            "job_type": list(x.value for x in self.job_type),
            "remote": list(x.value for x in self.remote),
            "location_name": self.location_name,
            "distance": self.distance,
            "limit": self.limit
        }
