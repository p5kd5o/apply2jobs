from typing import Optional

from pydantic import BaseModel, Field

from utils import patterns
from .apply_personal_contact_config import (
    ApplyPersonalContactConfig
)
from .apply_personal_demographic_config import (
    ApplyPersonalDemographicConfig
)
from .apply_personal_location_config import (
    ApplyPersonalLocationConfig
)
from .apply_personal_social_config import (
    ApplyPersonalSocialConfig
)


# pylint: disable=too-few-public-methods
class ApplyPersonalConfig(BaseModel, extra="forbid"):
    first_name: str
    last_name: str
    desired_salary: str = Field(pattern=f"^{patterns.CURRENCY_PATTERN}$")
    contact: ApplyPersonalContactConfig
    location: ApplyPersonalLocationConfig
    demographic: ApplyPersonalDemographicConfig
    social: Optional[ApplyPersonalSocialConfig] = ApplyPersonalSocialConfig()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
