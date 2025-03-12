from pydantic import BaseModel

from .apply_personal_config import ApplyPersonalConfig


class ApplyConfig(BaseModel, extra="forbid"):
    confirm_before_submit: bool
    personal: ApplyPersonalConfig

