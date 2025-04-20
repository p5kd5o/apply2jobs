from models.base_model import _BaseModel
from .personal import SubmitPersonalConfig


# pylint: disable=too-few-public-methods
class SubmitConfig(_BaseModel):
    confirm_before_submit: bool
    personal: SubmitPersonalConfig
