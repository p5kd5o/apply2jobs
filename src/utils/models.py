from enum import Enum


def ensure_enum(enum_type: Enum):
    def func(value: str) -> Enum:
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
