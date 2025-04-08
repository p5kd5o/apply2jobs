from typing import Sequence

from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import (
    Collection, DeleteResult, InsertOneResult, UpdateResult
)

from models.base_model import _BaseModel
from utils.strcase import CasedStr, CaseType

from .base_backend import _BaseBackend


class MongodbBackend(_BaseBackend):

    __client: MongoClient
    __database: Database

    def __init__(self, connection_string: str, table_case: CaseType = None):
        super().__init__(connection_string, table_case=table_case)
        self.__client = MongoClient(connection_string)
        self.__database = self.__client.get_database()

    @property
    def database(self) -> Database:
        return self.__database

    def collection(self, data_type: type) -> Collection:
        return self.__database[
            CasedStr(data_type.__name__).convert(to_case=self.table_case)
        ]

    def read_all(self, data_type: type) -> Sequence[_BaseModel]:
        return map(data_type, self.collection(data_type).find({}))

    def read(self, _id: ObjectId, data_type: type) -> _BaseModel | None:
        result = self.collection(data_type).find_one({"_id": _id})
        return None if result is None else data_type(result)

    def create(self, data: _BaseModel) -> InsertOneResult:
        return self.collection(type(data)).insert_one(data.model_dump())

    def update(
        self, _id: ObjectId, data: _BaseModel, upsert: bool = False
    ) -> UpdateResult:
        return self.collection(type(data)).update_one(
            {"_id": _id},
            {"$set": data.model_dump()},
            upsert=upsert
        )

    def delete(self, _id: ObjectId, data_type: type) -> DeleteResult:
        return self.collection(data_type).delete_one(
            {"_id": _id},
        )
