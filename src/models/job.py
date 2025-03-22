from typing import Annotated

from pydantic import AfterValidator, BaseModel, HttpUrl

from models.job_source import JobSource


# pylint: disable=too-few-public-methods
class Job(BaseModel, extra="forbid"):
    company_name: str
    title: str
    description: str
    apply_url: Annotated[HttpUrl, AfterValidator(str)]
    source: JobSource
