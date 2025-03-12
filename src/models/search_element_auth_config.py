from enum import Enum
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, ValidationError

from . import ensure_enum
from .search_element_auth_scheme_basic_config import SearchElementAuthSchemeBasicConfig
from .search_element_auth_scheme_oauth_config import SearchElementAuthSchemeOauthConfig


class SearchElementAuthScheme(Enum):
    BASIC = 1
    OAUTH = 2


class SearchElementAuthConfig(BaseModel, extra="forbid"):
    scheme: Annotated[
        SearchElementAuthScheme,
        BeforeValidator(ensure_enum(SearchElementAuthScheme))
    ]
    credentials: ( 
        SearchElementAuthSchemeBasicConfig |
        SearchElementAuthSchemeOauthConfig
    )
