from enum import Enum
from typing import Any


def ensure_enum(enum_type: Enum, data_type: type = object):
    def func(value: str) -> Enum:
        try:
            return enum_type[value]
        except (KeyError, ValueError):
            raise ValueError(
                "Value must be a member of "
                f"{{{', '.join(enum_type.__members__.keys())}}}"
            )
    return func

