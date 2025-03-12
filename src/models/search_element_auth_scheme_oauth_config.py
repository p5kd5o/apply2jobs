from pydantic import BaseModel

from .search_element_auth_credential_config import (
    SearchElementCredentialConfig
)


class SearchElementAuthSchemeOauthConfig(BaseModel, extra="forbid"):
      client_id: SearchElementCredentialConfig
      client_secret: SearchElementCredentialConfig
      token: SearchElementCredentialConfig
