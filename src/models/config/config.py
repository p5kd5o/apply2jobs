from typing import Optional

from models.base_model import _BaseModel
from utils.types import _Id
from .search import SearchConfig
from .submit import SubmitConfig


# pylint: disable=too-few-public-methods
class Config(_BaseModel):
    search: SearchConfig
    submit: SubmitConfig
    user_id: Optional[_Id] = None
