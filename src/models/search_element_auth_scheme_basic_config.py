from pydantic import BaseModel

from .search_element_auth_credential_config import (
    SearchElementCredentialConfig
 )


class SearchElementAuthSchemeBasicConfig(BaseModel, extra="forbid"):
    username: SearchElementCredentialConfig
    password: SearchElementCredentialConfig
