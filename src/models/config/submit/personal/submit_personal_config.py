from typing import Optional

from pydantic import Field

from .contact import SubmitPersonalContactConfig
from .demographic import SubmitPersonalDemographicConfig
from .location import SubmitPersonalLocationConfig
from .social import SubmitPersonalSocialConfig

from models.base_model import _BaseModel
from utils import patterns


# pylint: disable=too-few-public-methods
class SubmitPersonalConfig(_BaseModel):
    first_name: str
    last_name: str
    desired_salary: str = Field(pattern=f"^{patterns.CURRENCY_PATTERN}$")
    contact: SubmitPersonalContactConfig
    location: SubmitPersonalLocationConfig
    demographic: SubmitPersonalDemographicConfig
    social: Optional[SubmitPersonalSocialConfig] = SubmitPersonalSocialConfig()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
