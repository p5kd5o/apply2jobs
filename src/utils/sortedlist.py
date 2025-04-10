from operator import gt, lt
from sys import maxsize
from typing import Any, Callable, Iterable, Self, SupportsIndex

from utils.types import SupportsRichComparison


class SortedList[T: Any](list[T]):

    __key: Callable[[T], SupportsRichComparison[T]]
    __is_reversed: bool = False

    def __init__(
        self,
        iterable: Iterable = (),
        key: Callable[[T], SupportsRichComparison[T]] = None,
        reverse: bool = False
    ):
        super().__init__(sorted(iterable, key=key, reverse=reverse))
        if key is None:
            self.__key = lambda x: x
        else:
            self.__key = key
        self.__is_reversed = reverse

    @property
    def key(self) -> Callable[[T], SupportsRichComparison[T]]:
        return self.__key

    @property
    def is_reversed(self) -> bool:
        return self.__is_reversed

    def __add__(self, other) -> Self:
        cls = type(self)
        new = cls(
            self,
            key=self.key,
            reverse=self.is_reversed
        )
        new.extend(other)
        return new

    def __iadd__(self, other) -> Self:
        self.extend(other)
        return self

    def __contains__(self, value) -> bool:
        try:
            self.__binary_search(value)
        except ValueError:
            return False
        return True

    def __setitem__(self, index, value) -> None:
        self.insert(index, value)

    def __binary_search(
        self,
        value: T,
        *,
        start: SupportsIndex = 0,
        stop: SupportsIndex = maxsize,
        missing_ok: bool = False
    ) -> int:
        start = max(start, 0)
        stop = min(stop, len(self))
        index = (stop - start) // 2
        value_key = self.key(value)
        index_key = None
        is_before = gt if self.is_reversed else lt
        while start < stop:
            if index < len(self):
                index_key = self.key(self[index])
            if value_key == index_key:
                return index
            if is_before(value_key, index_key):
                stop = index
                index -= (stop - start + 1) // 2
            else:
                start = index + 1
                index += (stop - start) // 2 + 1
        if missing_ok:
            return index
        raise ValueError(f"{value} (key: {value_key}) is not in list")

    # pylint: disable=unused-argument
    def insert(self, index: SupportsIndex, value: T) -> None:
        self.append(value)

    def append(self, value: T) -> None:
        return super().insert(
            self.__binary_search(value, missing_ok=True),
            value
        )

    def extend(self, iterable: Iterable) -> None:
        for value in iterable:
            self.append(value)

    def remove(self, value: T) -> None:
        del self[self.index(value)]

    def index(
        self,
        value: T,
        start: SupportsIndex = 0,
        stop: SupportsIndex = maxsize
    ) -> int:
        index = self.__binary_search(value, start=start, stop=stop)
        first = index
        index = first - 1
        while index >= 0 and self[index] == value:
            first = index
            index -= 1
        return first

    def count(self, value: T) -> int:
        try:
            index = self.__binary_search(value)
        except ValueError:
            count = 0
        else:
            count = 1
            start = index
            index = start - 1
            while index >= 0 and self[index] == value:
                count += 1
                index -= 1
            index = start + 1
            while index < len(self) and self[index] == value:
                count += 1
                index += 1
        return count

    def sort(
        self,
        key: Callable[[T], SupportsRichComparison[T]] = None,
        reverse: bool = False
    ) -> None:
        super().sort(key=key, reverse=reverse)
        if key is None:
            self.__key = lambda x: x
        else:
            self.__key = key
        self.__is_reversed = reverse

    def reverse(self) -> None:
        super().reverse()
        self.__is_reversed = not self.__is_reversed
