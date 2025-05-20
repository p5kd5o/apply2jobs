from dataclasses import dataclass


@dataclass
class ResultWithErrors[T]:
    result: T
    errors: list[Exception]
