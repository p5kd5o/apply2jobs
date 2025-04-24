from typing import Annotated, Optional

from pydantic import AfterValidator, BeforeValidator, EmailStr, Field
from pydantic_extra_types.phone_numbers import (
    PhoneNumber, PhoneNumberValidator
)

from models.base_model import _BaseModel
from .password import Password

USERNAME_PATTERN = r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$"


# pylint: disable=too-few-public-methods
class User(_BaseModel):
    username: Annotated[
        str,
        Field(pattern=USERNAME_PATTERN, min_length=1, max_length=63)
    ]
    email_address: Annotated[
        str | EmailStr,
        BeforeValidator(lambda s: s.lower()),
        AfterValidator(str)
    ]
    phone_number: Optional[Annotated[
        str | PhoneNumber,
        PhoneNumberValidator(default_region="US"),
        AfterValidator(lambda s: s[s.find(":") + 1:])
    ]] = None
    password: Password
    federated: bool
