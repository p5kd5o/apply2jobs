from pydantic import BaseModel


# pylint: disable=too-few-public-methods
class ApplyPersonalLocationConfig(BaseModel, extra="forbid"):
    city: str
    state: str
    country: str
