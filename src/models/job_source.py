from pydantic import BaseModel, HttpUrl


class JobSource(BaseModel, extra="forbid"):
    shortname: str
    site: str
    url: str
    urn: str
