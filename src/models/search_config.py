from pydantic import BaseModel

from .search_element_config import SearchElementConfig


class SearchConfig(BaseModel, extra="forbid"):
    sites: list[SearchElementConfig]
