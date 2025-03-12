from pydantic import BaseModel

from .search_element_auth_credential_config import (
    SearchElementCredentialConfig
 )


# pylint: disable=too-few-public-methods
class SearchElementAuthSchemeBasicConfig(BaseModel, extra="forbid"):
    username: SearchElementCredentialConfig
    password: SearchElementCredentialConfig
