from typing import Annotated, Literal, Optional

from pydantic import AfterValidator, HttpUrl

from models.base_model import _BaseModel
from utils.types import _Id
from .field import Field


# pylint: disable=too-few-public-methods
class Form(_BaseModel):
    fields: list[Field]
    method: Literal["get", "post"]
    action: Annotated[HttpUrl, AfterValidator(str)]
    job_id: Optional[_Id] = None
