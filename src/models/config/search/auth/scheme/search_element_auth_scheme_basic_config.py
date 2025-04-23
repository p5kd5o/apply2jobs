from pydantic import Field

from models.base_model import _BaseModel
from ..credentials import SearchElementAuthCredentialConfig


# pylint: disable=too-few-public-methods
class SearchElementAuthSchemeBasicConfig(_BaseModel):
    username: SearchElementAuthCredentialConfig
    password: SearchElementAuthCredentialConfig = Field(exclude=True)
