from typing import Optional

from models.base_model import _BaseModel


# pylint: disable=too-few-public-methods
class SubmitPersonalDemographicConfig(_BaseModel):
    authorized_to_work: bool
    citizen: bool
    immigration_sponsorship: bool
    sex: Optional[str] = ""
    gender: Optional[str] = ""
    pronouns: Optional[str] = ""
    sexual_orientation: Optional[str] = ""
    transgender: Optional[bool] = None
    ethnicity: Optional[str] = ""
    races: Optional[list[str]] = []
    disability: Optional[bool] = None
    veteran: Optional[bool] = None

    @property
    def transgender_status(self):
        if self.transgender is None:
            return "I do not want to answer"
        if self.transgender:
            return "Yes"
        return "No"

    @property
    def disability_status(self):
        if self.disability is None:
            return "I do not want to answer"
        if self.disability:
            return "Yes"
        return "No"

    @property
    def hispanic_status(self):
        if self.ethnicity is None or self.ethnicity == "":
            return "Decline to self identify"
        if self.ethnicity.casefold() == "hispanic":
            return "Yes"
        return "No"

    @property
    def veteran_status(self):
        if self.veteran is None:
            return "I don't wish to answer"
        if self.veteran:
            return (
                "I identify as one or more of the classifications of a "
                "protected veteran"
            )
        return "I am not a protected veteran"
