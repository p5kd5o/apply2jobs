from enum import Enum
from typing import Annotated

from pydantic import BaseModel, BeforeValidator

from . import ensure_enum


class SearchElementCredentialValueType(Enum):
    PLAINTEXT = 1
    ENV = 2


# pylint: disable=too-few-public-methods
class SearchElementCredentialConfig(BaseModel, extra="forbid"):
    value_type: Annotated[
        SearchElementCredentialValueType,
        BeforeValidator(ensure_enum(SearchElementCredentialValueType))
    ] = SearchElementCredentialValueType.PLAINTEXT
    value: str
