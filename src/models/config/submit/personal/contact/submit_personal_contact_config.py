from typing import Annotated

from pydantic import AfterValidator, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from models.base_model import _BaseModel

# pylint: disable=too-few-public-methods
class SubmitPersonalContactConfig(_BaseModel):
    phone_number: Annotated[PhoneNumber, AfterValidator(str)]
    email_address: Annotated[EmailStr, AfterValidator(str)]
