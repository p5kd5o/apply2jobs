from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel, HttpUrl


# pylint: disable=too-few-public-methods
class ApplyPersonalSocialConfig(BaseModel, extra="forbid"):
    linkedin: Optional[Annotated[HttpUrl, AfterValidator(str)]] = ""
    github: Optional[Annotated[HttpUrl, AfterValidator(str)]] = ""
    website: Optional[Annotated[HttpUrl, AfterValidator(str)]] = ""
