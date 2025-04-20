from enum import StrEnum
from os import getenv
from typing import Annotated, Literal, Optional, Self

from pydantic import BeforeValidator, Field, model_validator

from models.base_model import _BaseModel
from utils.models import ensure_enum


class SearchElementAuthCredentialValueTypeEnum(StrEnum):
    PLAINTEXT = "PLAINTEXT"
    ENV = "ENV"


SearchElementAuthCredentialValueType = Literal[
    SearchElementAuthCredentialValueTypeEnum.PLAINTEXT,
    SearchElementAuthCredentialValueTypeEnum.ENV,
]


# pylint: disable=too-few-public-methods
class SearchElementAuthCredentialConfig(_BaseModel):
    value_type: Optional[Annotated[
        SearchElementAuthCredentialValueTypeEnum,
        BeforeValidator(ensure_enum(SearchElementAuthCredentialValueTypeEnum))
    ]] = SearchElementAuthCredentialValueTypeEnum.PLAINTEXT
    value: str = Field(exclude=True)

    @model_validator(mode="after")
    def load_value(self) -> Self:
        if self.value_type == SearchElementAuthCredentialValueTypeEnum.ENV:
            env_value = getenv(self.value)
            if env_value is None:
                raise ValueError(f"{self.value}: No such environment variable")
            self.value = env_value
        self.value_type = None
        return self
