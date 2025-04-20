from typing import Annotated, Optional

from pydantic import AfterValidator, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from models.base_model import _BaseModel


# pylint: disable=too-few-public-methods
class User(_BaseModel):
    username: str
    email_address: EmailStr
    phone_number: Optional[Annotated[PhoneNumber, AfterValidator(str)]] = None
