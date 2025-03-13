from pydantic import BaseModel

from .search_element_auth_credential_config import (
    SearchElementAuthCredentialConfig
)


# pylint: disable=too-few-public-methods
class SearchElementAuthSchemeOauthConfig(BaseModel, extra="forbid"):
    client_id: SearchElementAuthCredentialConfig
    client_secret: SearchElementAuthCredentialConfig
    token: SearchElementAuthCredentialConfig
