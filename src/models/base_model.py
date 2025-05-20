from typing import Self, Mapping

from pydantic import BaseModel

from utils.types import _Id


# pylint: disable=too-few-public-methods
class _BaseModel(BaseModel, extra="allow"):
    _id: _Id

    def __init__(self, *args, _id: _Id = None, **kwgs):
        super().__init__(*args, **kwgs)
        self._id = _id

    @classmethod
    def from_dict(cls, value: Mapping) -> Self:
        return cls(**value)
