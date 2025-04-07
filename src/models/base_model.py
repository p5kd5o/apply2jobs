from pydantic import BaseModel

from utils.types.id import _Id


# pylint: disable=too-few-public-methods
class _BaseModel(BaseModel, extra="forbid"):
    _id: _Id

    def __init__(self, *args, _id: _Id = None, **kwgs):
        super().__init__(*args, **kwgs)
        self._id = _id
