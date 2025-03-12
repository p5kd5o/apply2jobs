from pydantic import BaseModel

from .search_element_auth_config import SearchElementAuthConfig
from .search_element_job_config import SearchElementJobConfig


# pylint: disable=too-few-public-methods
class SearchElementConfig(BaseModel, extra="forbid"):
    host: str
    auth: SearchElementAuthConfig
    jobs: list[SearchElementJobConfig]
