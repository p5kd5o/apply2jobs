from enum import Enum
from typing import Any, Callable


def ensure_enum[T: Enum](enum_type: type[T]) -> Callable[[Any], T]:
    def func(value: Any) -> T:
        if isinstance(value, enum_type):
            return value
        if value in enum_type:
            return enum_type(value)
        try:
            return enum_type[value]
        except KeyError as exc:
            enum_keys = enum_type.__members__.keys()
            enum_values = (
                member.value for member in
                enum_type.__members__.values()
            )
            enum_pairs = zip(enum_keys, enum_values)
            raise ValueError(
                "Value must be a member of "
                f"{{{', '.join(map(str, enum_pairs))}}}"
            ) from exc
    return func
