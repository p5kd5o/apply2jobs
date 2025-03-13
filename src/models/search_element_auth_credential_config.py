from enum import Enum
from typing import Annotated

from pydantic import BaseModel, BeforeValidator

from utils.models import ensure_enum


class SearchElementAuthCredentialValueType(Enum):
    PLAINTEXT = 1
    ENV = 2


# pylint: disable=too-few-public-methods
class SearchElementAuthCredentialConfig(BaseModel, extra="forbid"):
    value_type: Annotated[
        SearchElementAuthCredentialValueType,
        BeforeValidator(ensure_enum(SearchElementAuthCredentialValueType))
    ] = SearchElementAuthCredentialValueType.PLAINTEXT
    value: str
