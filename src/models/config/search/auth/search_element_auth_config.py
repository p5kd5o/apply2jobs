from enum import Enum
from typing import Annotated

from pydantic import AfterValidator, BeforeValidator, Field

from utils.models import ensure_enum

from models.base_model import _BaseModel
from .scheme import (
    SearchElementAuthSchemeBasicConfig,
    SearchElementAuthSchemeOauthConfig,
)


class SearchElementAuthScheme(Enum):
    BASIC = 1
    OAUTH = 2


# pylint: disable=too-few-public-methods
class SearchElementAuthConfig(_BaseModel):
    scheme: Annotated[
        SearchElementAuthScheme,
        BeforeValidator(ensure_enum(SearchElementAuthScheme)),
        AfterValidator(lambda e: e.value)
    ]
    credentials: (
        SearchElementAuthSchemeBasicConfig |
        SearchElementAuthSchemeOauthConfig
    ) = Field(exclude=True)
