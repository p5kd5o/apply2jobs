from models.base_model import _BaseModel


# pylint: disable=too-few-public-methods
class JobSource(_BaseModel):
    shortname: str
    site: str
    url: str
    urn: str
