from models.base_model import _BaseModel
from ..credentials import SearchElementAuthCredentialConfig


# pylint: disable=too-few-public-methods
class SearchElementAuthSchemeOauthConfig(_BaseModel):
    client_id: SearchElementAuthCredentialConfig
    client_secret: SearchElementAuthCredentialConfig
    token: SearchElementAuthCredentialConfig
