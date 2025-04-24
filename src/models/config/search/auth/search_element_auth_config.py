from enum import Enum, StrEnum
from typing import Annotated, Any

from pydantic import (
    BeforeValidator, Field, SerializationInfo, field_serializer
)

from utils.models import ensure_enum

from models.base_model import _BaseModel
from .scheme import (
    SearchElementAuthSchemeBasicConfig,
    SearchElementAuthSchemeOauthConfig,
)


class SearchElementAuthScheme(StrEnum):
    BASIC = "basic"
    OAUTH = "oauth"


# pylint: disable=too-few-public-methods
class SearchElementAuthConfig(_BaseModel):
    scheme: Annotated[
        SearchElementAuthScheme,
        BeforeValidator(ensure_enum(SearchElementAuthScheme))
    ]
    credentials: Annotated[
        SearchElementAuthSchemeBasicConfig |
        SearchElementAuthSchemeOauthConfig,
        Field(exclude=True)
    ]

    @field_serializer("scheme")
    def _serialize_enum(self, field_value: Enum, _: SerializationInfo) -> Any:
        return field_value.value
