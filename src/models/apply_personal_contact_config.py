from typing import Annotated

from pydantic import AfterValidator, BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


# pylint: disable=too-few-public-methods
class ApplyPersonalContactConfig(BaseModel, extra="forbid"):
    phone_number: Annotated[PhoneNumber, AfterValidator(str)]
    email_address: Annotated[EmailStr, AfterValidator(str)]
