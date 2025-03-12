from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class ApplyPersonalContactConfig(BaseModel, extra="forbid"):
    phone_number: PhoneNumber
    email_address: EmailStr
