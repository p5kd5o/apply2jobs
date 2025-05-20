from enum import Enum, StrEnum
from typing import Annotated, Any, Optional

from pydantic import BeforeValidator, SerializationInfo, field_serializer

from models.base_model import _BaseModel
from utils.enums import ensure_enum


class InputTypeEnum(StrEnum):
    BUTTON = "button"
    CHECKBOX = "checkbox"
    COLOR = "color"
    DATE = "date"
    DATETIME = "datetime"
    DATETIME_LOCAL = "datetime-local"
    EMAIL = "email"
    FILE = "file"
    HIDDEN = "hidden"
    IMAGE = "image"
    MONTH = "month"
    NUMBER = "number"
    PASSWORD = "password"
    RADIO = "radio"
    RANGE = "range"
    RESET = "reset"
    SEARCH = "search"
    SUBMIT = "submit"
    TEL = "tel"
    TEXT = "text"
    TIME = "time"
    URL = "url"
    WEEK = "week"


# pylint: disable=too-few-public-methods
class Field(_BaseModel):
    input_id: str
    input_name: Optional[str]
    input_type: Annotated[
        InputTypeEnum,
        BeforeValidator(ensure_enum(InputTypeEnum))
    ]
    input_label: Optional[str] = None
    input_value: Optional[str] = None

    @field_serializer("input_type")
    def _serialize_enum(self, field_value: Enum, _: SerializationInfo) -> Any:
        return field_value.value
