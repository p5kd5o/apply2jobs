from .base_model import _BaseModel
from .apply_config import ApplyConfig
from .search_config import SearchConfig


# pylint: disable=too-few-public-methods
class Config(_BaseModel):
    search: SearchConfig
    apply: ApplyConfig
