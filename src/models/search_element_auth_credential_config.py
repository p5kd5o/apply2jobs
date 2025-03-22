from enum import Enum
from typing import Annotated, Optional

from pydantic import (
    BaseModel, BeforeValidator, Field, SerializationInfo, field_serializer
)

from utils.models import ensure_enum


class SearchElementAuthCredentialValueType(Enum):
    PLAINTEXT = 1
    ENV = 2


# pylint: disable=too-few-public-methods
class SearchElementAuthCredentialConfig(BaseModel, extra="forbid"):
    value_type: Optional[Annotated[
        SearchElementAuthCredentialValueType,
        BeforeValidator(ensure_enum(SearchElementAuthCredentialValueType))
    ]] = SearchElementAuthCredentialValueType.PLAINTEXT
    value: str = Field(exclude=True)

    @field_serializer("value_type")
    def _serialize_value_type(
        self,
        value_type: SearchElementAuthCredentialValueType,
        _: SerializationInfo
    ) -> str:
        return value_type.name
