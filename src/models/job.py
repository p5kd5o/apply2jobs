from copy import deepcopy
from typing import Annotated

from pydantic import AfterValidator, BaseModel, HttpUrl

from models.job_source import JobSource


class Job(BaseModel, extra="forbid"):
    company_name: str
    title: str
    description: str
    apply_url: Annotated[HttpUrl, AfterValidator(str)]
    source: JobSource

    def __init__(
            self,
            company_name: str,
            title: str,
            description: str,
            apply_url: HttpUrl,
            source: JobSource
    ):
        super().__init__(
            company_name=company_name,
            title=title,
            description=description,
            apply_url=apply_url,
            source=deepcopy(source)
        )
