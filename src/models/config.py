from pydantic import BaseModel

from .apply_config import ApplyConfig
from .search_config import SearchConfig


class Config(BaseModel, extra="forbid"):
    search: SearchConfig
    apply: ApplyConfig

