from utils.types.id import _Id

from models.base_model import _BaseModel
from .search import SearchConfig
from .submit import SubmitConfig


# pylint: disable=too-few-public-methods
class Config(_BaseModel):
    search: SearchConfig
    submit: SubmitConfig
    _user_id: _Id | None = None
