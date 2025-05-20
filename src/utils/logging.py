from enum import Enum
from typing import Any, Literal, Mapping
import logging

from utils.enums import ensure_enum


class LevelEnum(Enum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


LevelType = Literal[
    LevelEnum.CRITICAL,
    LevelEnum.ERROR,
    LevelEnum.WARNING,
    LevelEnum.INFO,
    LevelEnum.DEBUG,
]


class ColorEnum(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    DEFAULT = 9


ColorType = Literal[
    ColorEnum.BLACK,
    ColorEnum.RED,
    ColorEnum.GREEN,
    ColorEnum.YELLOW,
    ColorEnum.BLUE,
    ColorEnum.MAGENTA,
    ColorEnum.CYAN,
    ColorEnum.WHITE,
]


class ColorFormatter(logging.Formatter):
    """Color messages based on level name."""
    __colors: dict[LevelType, ColorType] = {
        LevelEnum.CRITICAL: ColorEnum.MAGENTA,
        LevelEnum.ERROR: ColorEnum.RED,
        LevelEnum.WARNING: ColorEnum.YELLOW,
        LevelEnum.INFO: ColorEnum.DEFAULT,
        LevelEnum.DEBUG: ColorEnum.BLUE,
    }

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: str = "%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
        colors: Mapping[LevelType, ColorType] | None = None
    ):
        """Iniitalize a colored formatter."""
        super().__init__(
            fmt, datefmt, style, validate, defaults=defaults
        )
        if colors is not None:
            self.colors = colors

    @property
    def colors(self) -> dict[LevelType, ColorType]:
        return self.__colors.copy()

    @colors.setter
    def colors(self, value: Mapping[LevelType, ColorType]):
        self.__colors = {
            ensure_enum(LevelEnum)(level): ensure_enum(ColorEnum)(color)
            for level, color in value.items()
        }

    def format(self, record: logging.LogRecord):
        """Format and color a log message."""
        level = LevelEnum[record.levelname]
        color = self.__colors.get(level, ColorEnum.DEFAULT)
        parts = [
            f"{0x1b:c}[{30 + color.value}m",
            super().format(record),
            f"{0x1b:c}[{30 + ColorEnum.DEFAULT.value}m"
        ]
        return "".join(parts)
