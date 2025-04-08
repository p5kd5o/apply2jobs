import abc
from typing import Sequence

from models.base_model import _BaseModel
from utils.strcase import CaseEnum, CaseType
from utils.types.id import _Id


class _BaseBackend(abc.ABC):

    __table_case: str = CaseEnum.SNAKE.value

    @abc.abstractmethod
    def __init__(
        self, connection_string: str, table_case: CaseType | str = None
    ):
        super().__init__()
        if table_case is not None:
            self.table_case = table_case

    @property
    def table_case(self) -> str:
        return self.__table_case

    @table_case.setter
    def table_case(self, value: CaseType | str) -> CaseType:
        if isinstance(value, CaseType):
            self.__table_case = value.value
        elif value in CaseEnum:
            self.__table_case = value
        else:
            raise ValueError(
                f"got {value}, expected one of "
                f"{{"
                f"{','.join(e.value for e in CaseEnum.__members__.values())}"
                f"}}"
            )

    @abc.abstractmethod
    def create(self, value: _BaseModel) -> object:
        pass

    @abc.abstractmethod
    def create_many(
        self, data_type: type, *values: _BaseModel
    ) -> Sequence[object]:
        pass

    @abc.abstractmethod
    def get(self, data_type: type, _id: _Id) -> _BaseModel | None:
        pass

    @abc.abstractmethod
    def find(
        self, data_type: type, constraints: dict[str, object]
    ) -> Sequence[_BaseModel]:
        pass

    @abc.abstractmethod
    def update(
        self, _id: _Id, value: _BaseModel, upsert: bool = False
    ) -> object:
        pass

    @abc.abstractmethod
    def delete(self, data_type: type, _id: _Id) -> object:
        pass

    @abc.abstractmethod
    def delete_many(self, data_type: type, *_ids: _Id) -> Sequence[object]:
        pass
