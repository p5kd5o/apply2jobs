from pydantic import BaseModel

from .search_element_config import SearchElementConfig


# pylint: disable=too-few-public-methods
class SearchConfig(BaseModel, extra="forbid"):
    sites: list[SearchElementConfig]
