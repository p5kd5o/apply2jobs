import abc

from models.base_model import _BaseModel
from utils.strcase import CaseType
from utils.types.id import _Id


class _BaseBackend(abc.ABC):

    __table_case: CaseType = "snake"

    def __init__(self, table_case: CaseType = None):
        super().__init__()
        if table_case is not None:
            self.__table_case = table_case

    @property
    def table_case(self) -> CaseType:
        return self.__table_case.value

    @abc.abstractmethod
    def read(self, _id: _Id, data_type: type) -> _BaseModel:
        pass

    @abc.abstractmethod
    def create(self, data: _BaseModel) -> object:
        pass

    @abc.abstractmethod
    def update(
        self, _id: _Id, data: _BaseModel, upsert: bool = False
    ) -> object:
        pass

    @abc.abstractmethod
    def delete(self, _id: _Id, data_type: type) -> object:
        pass
