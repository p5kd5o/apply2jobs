from enum import Enum
from typing import Annotated, Optional

from pydantic import (
     BeforeValidator, Field, SerializationInfo, field_serializer
)

from utils.models import ensure_enum

from .base_model import _BaseModel


class SearchElementAuthCredentialValueType(Enum):
    PLAINTEXT = 1
    ENV = 2


# pylint: disable=too-few-public-methods
class SearchElementAuthCredentialConfig(_BaseModel):
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
