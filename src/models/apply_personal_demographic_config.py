from pydantic import BaseModel


# pylint: disable=too-few-public-methods
class ApplyPersonalDemographicConfig(BaseModel, extra="forbid"):
    sex: str
    gender: str
    sexual_orientation: str
    transgender: bool
    races: list[str]
    ethnicity: str
    disability: bool
    veteran: bool
