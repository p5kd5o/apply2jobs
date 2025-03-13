from pydantic import BaseModel

from .search_element_auth_credential_config import (
    SearchElementAuthCredentialConfig
 )


# pylint: disable=too-few-public-methods
class SearchElementAuthSchemeBasicConfig(BaseModel, extra="forbid"):
    username: SearchElementAuthCredentialConfig
    password: SearchElementAuthCredentialConfig
