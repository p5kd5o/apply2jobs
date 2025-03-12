from enum import Enum
from typing import Any


def ensure_enum(enum_type: Enum):
    def func(value: str) -> Enum:
        try:
            return enum_type[value]
        except (KeyError, ValueError) as exc:
            raise ValueError(
                "Value must be a member of "
                f"{{{', '.join(enum_type.__members__.keys())}}}"
            ) from exc
    return func
