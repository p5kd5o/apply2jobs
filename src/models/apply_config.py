from pydantic import BaseModel

from .apply_personal_config import ApplyPersonalConfig


# pylint: disable=too-few-public-methods
class ApplyConfig(BaseModel, extra="forbid"):
    confirm_before_submit: bool
    personal: ApplyPersonalConfig
