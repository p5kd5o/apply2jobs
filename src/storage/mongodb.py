from typing import Sequence

from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from models.base_model import _BaseModel
from utils.strcase import CasedStr, CaseType
from .base_backend import _BaseBackend
from .results import (
    CreateOneResult, CreateManyResult, UpdateResult, DeleteResult
)


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

    def create(self, value: _BaseModel) -> CreateOneResult:
        result = self.collection(type(value)).insert_one(value.model_dump())
        return CreateOneResult(created_id=result.inserted_id)

    def create_many(
        self, data_type: type, *values: _BaseModel
    ) -> CreateManyResult:
        result = self.collection(data_type).insert_many(
            value.model_dump() for value in values
        )
        return CreateManyResult(
            created_count=len(result.inserted_ids),
            created_ids=result.inserted_ids
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
        result = self.collection(type(value)).update_one(
            {"_id": _id},
            {"$set": value.model_dump()},
            upsert=upsert
        )
        return UpdateResult(
            matched_count=result.matched_count,
            did_upsert=result.did_upsert,
            upserted_id=result.upserted_id
        )

    def delete(self, data_type: type, _id: ObjectId) -> DeleteResult:
        result = self.collection(data_type).delete_one(
            {"_id": _id}
        )
        return DeleteResult(deleted_count=result.deleted_count)

    def delete_many(self, data_type: type, *_ids: ObjectId) -> DeleteResult:
        result = self.collection(data_type).delete_many(
            {"_id": {"$in": list(_ids)}}
        )
        return DeleteResult(deleted_count=result.deleted_count)
