from enum import StrEnum
from typing import Callable, Literal, Self


class CaseEnum(StrEnum):
    SNAKE = "snake"
    KEBAB = "kebab"
    CAMEL = "camel"
    PASCAL = "pascal"


CaseType = Literal[
    CaseEnum.SNAKE,
    CaseEnum.KEBAB,
    CaseEnum.CAMEL,
    CaseEnum.PASCAL,
]


class CasedStr(str):

    __case: CaseType | None

    # pylint: disable=unused-argument
    def __init__(
        self, value: str = "", encoding: str = None, errors: str = None
    ):
        self.__case = self.detect_case(self)

    @property
    def case(self) -> str:
        return self.__case.value

    def convert(self, to_case: CaseType) -> Self:
        return CasedStr(
            "" if len(self) == 0 else
            self.__join_func(to_case)(self.__split_func(self.case)(self))
        )

    @staticmethod
    def detect_case(value: str) -> CaseType | None:
        if len(value) > 0:
            if "_" in value:
                return CaseEnum.SNAKE
            if "-" in value:
                return CaseEnum.KEBAB
            if value[0].isupper():
                return CaseEnum.PASCAL
            return CaseEnum.CAMEL
        return None

    @classmethod
    def __split_func(cls, case: CaseType) -> Callable[[str], list[str]]:
        try:
            return {
                CaseEnum.SNAKE:
                lambda string: string.split("_"),
                CaseEnum.KEBAB:
                lambda string: string.split("-"),
                CaseEnum.CAMEL:
                cls.__split_camel,
                CaseEnum.PASCAL:
                cls.__split_camel,
            }[case]
        except KeyError as exc:
            raise ValueError(
                f"``case'' must be one of {set(map(
                    lambda e: e.value,
                    CaseEnum.__members__.values()
                ))}"
            ) from exc

    # pylint: disable=unnecessary-direct-lambda-call
    @classmethod
    def __join_func(cls, case: CaseType) -> Callable[[list[str]], str]:
        try:
            return {
                CaseEnum.SNAKE:
                lambda words: "_".join(word.lower() for word in words),
                CaseEnum.KEBAB:
                lambda words: "-".join(word.lower() for word in words),
                CaseEnum.CAMEL: (
                    lambda cls:
                    lambda words: cls.__join_camel(words, pascal=False)
                )(cls),
                CaseEnum.PASCAL: (
                    lambda cls:
                    lambda words: cls.__join_camel(words, pascal=True)
                )(cls),
            }[case]
        except KeyError as exc:
            raise ValueError(
                f"``case'' must be one of {set(map(
                    lambda e: e.value,
                    CaseEnum.__members__.values()
                ))}"
            ) from exc

    @classmethod
    def __find_next_sep(
        cls, value: str, index: int, is_sep: Callable[[str], bool]
    ) -> int:
        return (
            index if index >= len(value) or is_sep(value[index]) else
            cls.__find_next_sep(value, index + 1, is_sep)
        )

    @classmethod
    def __split_camel(cls, value: str, start: int = 0) -> list[str]:
        if start < len(value):
            next_sep = cls.__find_next_sep(
                value, start + 1, lambda char: char.isupper()
            )
            return [
                value[start:next_sep]
            ] + cls.__split_camel(value, start=next_sep)
        return []

    @staticmethod
    def __join_camel(words: list[str], pascal: bool = False) -> str:
        return (
            "" if len(words) == 0 else
            "".join(w.title() for w in words) if pascal else
            "".join(
                [words[0].lower()] +
                [w.title() for w in words[1:]]
            )
        )
