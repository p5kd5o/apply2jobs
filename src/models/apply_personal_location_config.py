from typing import Annotated

from pydantic import AfterValidator, BeforeValidator, Field

from .base_model import _BaseModel


# pylint: disable=too-few-public-methods
class ApplyPersonalLocationConfig(_BaseModel):
    street_address: Annotated[
        str | list[str], AfterValidator(
            lambda x: ", ".join(x) if isinstance(x, list) else x
        )
    ]
    city: str
    state: str
    zip_code: Annotated[str, BeforeValidator(str)] = Field(
        pattern=r"^([0-9]+[0-9-]?[0-9]+)+$"
    )
    country: str

    # pylint: disable=too-many-arguments
    def to_str(
        self,
        *,
        street_address: bool = True,
        city: bool = True,
        state: bool = True,
        zip_code: bool = True,
        country: bool = True
    ):
        elements = []
        if street_address:
            elements.append(self.street_address)
        if city:
            elements.append(self.city)
        if state and zip_code:
            elements.append(f"{self.state} {self.zip_code}")
        elif state:
            elements.append(self.state)
        elif zip_code:
            elements.append(self.zip_code)
        if country:
            elements.append(self.country)
        return ", ".join(elements)
