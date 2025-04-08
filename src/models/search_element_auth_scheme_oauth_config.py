from .base_model import _BaseModel
from .search_element_auth_credential_config import (
    SearchElementAuthCredentialConfig
)


# pylint: disable=too-few-public-methods
class SearchElementAuthSchemeOauthConfig(_BaseModel):
    client_id: SearchElementAuthCredentialConfig
    client_secret: SearchElementAuthCredentialConfig
    token: SearchElementAuthCredentialConfig
