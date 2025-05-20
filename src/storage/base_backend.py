import abc
from typing import Iterator

from models.base_model import _BaseModel
from utils.enums import ensure_enum
from utils.strcase import CaseEnum, CaseType
from utils.types import _Id
from .results import (
    CreateOneResult, CreateManyResult, UpdateResult, DeleteResult
)


class _BaseBackend(abc.ABC):

    __table_case: str = CaseEnum.SNAKE.value

    @abc.abstractmethod
    def __init__(
        self,
        connection_string: str,
        table_case: CaseType | str = None
    ):
        super().__init__()
        if table_case is not None:
            self.table_case = table_case

    @property
    def table_case(self) -> str:
        return self.__table_case

    @table_case.setter
    def table_case(self, value: CaseType | str) -> None:
        self.__table_case = ensure_enum(CaseEnum)(value).value

    @abc.abstractmethod
    def create(self, value: _BaseModel) -> CreateOneResult:
        pass

    @abc.abstractmethod
    def create_many(
        self, data_type: type, *values: _BaseModel
    ) -> CreateManyResult:
        pass

    @abc.abstractmethod
    def get(self, data_type: type, _id: _Id) -> _BaseModel | None:
        pass

    @abc.abstractmethod
    def find(
        self, data_type: type, constraints: dict[str, object]
    ) -> Iterator[_BaseModel]:
        pass

    @abc.abstractmethod
    def update(
        self, _id: _Id, value: _BaseModel, upsert: bool = False
    ) -> UpdateResult:
        pass

    @abc.abstractmethod
    def delete(self, data_type: type, _id: _Id) -> DeleteResult:
        pass

    @abc.abstractmethod
    def delete_many(self, data_type: type, *_ids: _Id) -> DeleteResult:
        pass
