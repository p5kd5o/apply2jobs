from typing import Optional

from models.base_model import _BaseModel
from .job_source import JobSource


# pylint: disable=too-few-public-methods
class Job(_BaseModel):
    company_name: str
    title: str
    description: str
    apply_url: Optional[str] = None
    source: JobSource
