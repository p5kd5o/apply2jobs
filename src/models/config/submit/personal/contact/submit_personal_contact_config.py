from typing import Annotated

from pydantic import AfterValidator, BeforeValidator, EmailStr
from pydantic_extra_types.phone_numbers import (
    PhoneNumber, PhoneNumberValidator
)

from models.base_model import _BaseModel


# pylint: disable=too-few-public-methods
class SubmitPersonalContactConfig(_BaseModel):
    email_address: Annotated[
        str | EmailStr,
        BeforeValidator(lambda s: s.lower()),
        AfterValidator(str)
    ]
    phone_number: Annotated[
        str | PhoneNumber,
        PhoneNumberValidator(default_region="US"),
        AfterValidator(lambda s: s[s.find(":") + 1:])
    ]
