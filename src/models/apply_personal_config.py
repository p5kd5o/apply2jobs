from pydantic import BaseModel

from .apply_personal_contact_config import (
    ApplyPersonalContactConfig
)
from .apply_personal_demographic_config import (
    ApplyPersonalDemographicConfig
)
from .apply_personal_location_config import (
    ApplyPersonalLocationConfig
)


class ApplyPersonalConfig(BaseModel, extra="forbid"):
    first_name: str
    last_name: str
    contact: ApplyPersonalContactConfig
    location: ApplyPersonalLocationConfig
    demographic: ApplyPersonalDemographicConfig
