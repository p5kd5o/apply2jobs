from typing import Annotated

from pydantic import AfterValidator, HttpUrl

from .base_model import _BaseModel
from .job_source import JobSource


# pylint: disable=too-few-public-methods
class Job(_BaseModel):
    company_name: str
    title: str
    description: str
    apply_url: Annotated[HttpUrl, AfterValidator(str)]
    source: JobSource
