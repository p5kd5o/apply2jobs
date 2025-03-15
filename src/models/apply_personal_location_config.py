from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field


# pylint: disable=too-few-public-methods
class ApplyPersonalLocationConfig(BaseModel, extra="forbid"):
    street_address: str
    street_address_line_2: Optional[str] = None
    city: str
    state: str
    zip_code: Annotated[str, BeforeValidator(str)] = Field(
        pattern=r"^[0-9]{5}$"
    )
    country: str

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
            if self.street_address_line_2 is not None:
                elements.append(self.street_address_line_2)
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
