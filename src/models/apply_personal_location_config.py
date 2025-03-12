from pydantic import BaseModel


class ApplyPersonalLocationConfig(BaseModel, extra="forbid"):
    city: str
    state: str
    country: str
