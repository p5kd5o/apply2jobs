from typing import Annotated, Optional

from pydantic import Field

from utils import patterns
from models.base_model import _BaseModel

from .contact import SubmitPersonalContactConfig
from .demographic import SubmitPersonalDemographicConfig
from .location import SubmitPersonalLocationConfig
from .social import SubmitPersonalSocialConfig


# pylint: disable=too-few-public-methods
class SubmitPersonalConfig(_BaseModel):
    first_name: str
    last_name: str
    desired_salary: Annotated[str, Field(pattern=f"^{patterns.CURRENCY_PATTERN}$")]
    contact: SubmitPersonalContactConfig
    location: SubmitPersonalLocationConfig
    demographic: SubmitPersonalDemographicConfig
    social: Optional[SubmitPersonalSocialConfig] = SubmitPersonalSocialConfig()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
