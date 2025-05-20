from typing import Annotated, Optional

from pydantic import AfterValidator, BeforeValidator, EmailStr, StringConstraints
from pydantic_extra_types.phone_numbers import (
    PhoneNumber, PhoneNumberValidator
)

from models.base_model import _BaseModel

from .password import Password

USERNAME_PATTERN = r"^[A-Za-z0-9_][A-Za-z0-9._-]*[A-Za-z0-9_]$"


# pylint: disable=too-few-public-methods
class User(_BaseModel):
    username: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            max_length=64,
            pattern=USERNAME_PATTERN
        )
    ]
    email_address: Annotated[
        EmailStr,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
        )
    ]
    password: Password
    federated: bool
    phone_number: Optional[Annotated[
        str | PhoneNumber,
        PhoneNumberValidator(default_region="US")
    ]] = None
