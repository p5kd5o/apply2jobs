from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.collection import (
    Collection, DeleteResult, InsertOneResult, UpdateResult
)

from models.base_model import _BaseModel
from utils.strcase import CasedStr, CaseType

from .base_backend import _BaseBackend


class MongodbBackend(_BaseBackend):

    __database: Database

    def __init__(self, database: Database, table_case: CaseType = None):
        super().__init__(table_case=table_case)
        self.__database = database

    @property
    def database(self) -> Database:
        return self.__database

    def collection(self, data_type: type) -> Collection:
        return self.__database[
            CasedStr(data_type.__name__).convert(to_case=self.table_case)
        ]

    def read(self, _id: ObjectId, data_type: type) -> _BaseModel:
        return self.collection(data_type).find_one({"_id": _id})

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
