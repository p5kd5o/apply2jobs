from pydantic import BaseModel, Field


# pylint: disable=too-few-public-methods
class ApplyPersonalLocationConfig(BaseModel, extra="forbid"):
    street: str
    city: str
    state: str
    zip_code: str = Field(pattern=r"^[0-9]{5}$")
    country: str
