from typing import Annotated, Optional

from pydantic import AfterValidator, HttpUrl

from models.base_model import _BaseModel


# pylint: disable=too-few-public-methods
class SubmitPersonalSocialConfig(_BaseModel):
    linkedin: Optional[Annotated[HttpUrl, AfterValidator(str)]] = ""
    github: Optional[Annotated[HttpUrl, AfterValidator(str)]] = ""
    website: Optional[Annotated[HttpUrl, AfterValidator(str)]] = ""
