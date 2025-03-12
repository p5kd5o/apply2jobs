from pydantic import BaseModel


class ApplyPersonalDemographicConfig(BaseModel, extra="forbid"):
    sex: str
    gender: str
    sexual_orientation: str
    transgender: bool
    races: list[str]
    ethnicity: str
    disability: bool
    veteran: bool
