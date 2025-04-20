from models.base_model import _BaseModel
from .auth import SearchElementAuthConfig
from .jobs import SearchElementJobConfig


# pylint: disable=too-few-public-methods
class SearchElementConfig(_BaseModel):
    host: str
    auth: SearchElementAuthConfig
    jobs: list[SearchElementJobConfig]
