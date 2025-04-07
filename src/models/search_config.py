from .base_model import _BaseModel
from .search_element_config import SearchElementConfig


# pylint: disable=too-few-public-methods
class SearchConfig(_BaseModel):
    sites: list[SearchElementConfig]
