from pydantic import BaseModel

from .apply_config import ApplyConfig
from .search_config import SearchConfig


# pylint: disable=too-few-public-methods
class Config(BaseModel, extra="forbid"):
    search: SearchConfig
    apply: ApplyConfig
