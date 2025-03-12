from pydantic import BaseModel


# pylint: disable=too-few-public-methods
class JobSource(BaseModel, extra="forbid"):
    shortname: str
    site: str
    url: str
    urn: str
