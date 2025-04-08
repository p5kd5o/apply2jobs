from typing import Sequence

from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import (
    Collection, DeleteResult, InsertManyResult, InsertOneResult, UpdateResult
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

    def create(self, value: _BaseModel) -> InsertOneResult:
        return self.collection(type(value)).insert_one(value.model_dump())

    def create_many(
        self, data_type: type, *values: _BaseModel
    ) -> InsertManyResult:
        return self.collection(data_type).insert_many(
            value.model_dump() for value in values
        )

    def get(self, data_type: type, _id: ObjectId) -> _BaseModel | None:
        result = self.collection(data_type).find_one({"_id": _id})
        return None if result is None else data_type.from_dict(result)

    def find(
        self, data_type: type, constraints: dict[str, object]
    ) -> Sequence[_BaseModel]:
        return map(
            data_type.from_dict,
            self.collection(data_type).find(constraints)
        )

    def update(
        self, _id: ObjectId, value: _BaseModel, upsert: bool = False
    ) -> UpdateResult:
        return self.collection(type(value)).update_one(
            {"_id": _id},
            {"$set": value.model_dump()},
            upsert=upsert
        )

    def delete(self, data_type: type, _id: ObjectId) -> DeleteResult:
        return self.collection(data_type).delete_one(
            {"_id": _id}
        )

    def delete_many(self, data_type: type, *_ids: ObjectId) -> DeleteResult:
        return self.collection(data_type).delete_many(
            {"_id": {"$in": list(_ids)}}
        )
