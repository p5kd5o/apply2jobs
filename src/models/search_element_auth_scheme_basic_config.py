from .base_model import _BaseModel
from .search_element_auth_credential_config import (
    SearchElementAuthCredentialConfig
 )


# pylint: disable=too-few-public-methods
class SearchElementAuthSchemeBasicConfig(_BaseModel):
    username: SearchElementAuthCredentialConfig
    password: SearchElementAuthCredentialConfig
