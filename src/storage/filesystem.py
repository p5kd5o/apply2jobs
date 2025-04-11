import json
import pathlib
from urllib.parse import unquote, urlparse
from uuid import UUID, uuid4
from typing import Iterable

from models.base_model import _BaseModel
from utils.strcase import CasedStr, CaseType
from utils.mappings import filter_subset
from .base_backend import _BaseBackend
from .results import (
    CreateOneResult, CreateManyResult, UpdateResult, DeleteResult
)


class FilesystemBackend(_BaseBackend):

    __directory: pathlib.Path

    def __init__(self, connection_string: str, table_case: CaseType = None):
        super().__init__(connection_string, table_case=table_case)
        file_url = urlparse(unquote(connection_string))
        self.__directory = pathlib.Path(file_url.path)
        self.__directory.mkdir(exist_ok=True)

    @property
    def directory(self) -> pathlib.Path:
        return self.__directory

    def filepath(self, data_type: type) -> pathlib.Path:
        return (
            self.__directory /
            CasedStr(data_type.__name__).convert(to_case=self.table_case)
        ).with_suffix(".json")

    def create(self, value: _BaseModel) -> CreateOneResult:
        filepath = self.filepath(type(value))
        try:
            filedata = json.loads(filepath.read_text())
        except FileNotFoundError:
            filedata = []
        new_uuid = uuid4()
        new_data = {**value.model_dump(mode="json"), "_id": str(new_uuid)}
        filepath.write_text(json.dumps([*filedata, new_data]))
        return CreateOneResult(created_id=new_uuid)

    def create_many(
        self, data_type: type, *values: _BaseModel
    ) -> CreateManyResult:
        filepath = self.filepath(data_type)
        try:
            filedata = json.loads(filepath.read_text())
        except FileNotFoundError:
            filedata = []
        uuids = []
        for value in values:
            new_uuid = uuid4()
            new_data = {**value.model_dump(mode="json"), "_id": str(new_uuid)}
            uuids.append(new_uuid)
            filedata.append(new_data)
        filepath.write_text(json.dumps(filedata))
        return CreateManyResult(
            created_count=len(uuids), created_ids=uuids
        )

    def get(self, data_type: type, _id: UUID) -> _BaseModel | None:
        filepath = self.filepath(data_type)
        try:
            filedata = json.loads(filepath.read_text())
        except FileNotFoundError:
            filedata = []
        target = str(_id)
        for value in filedata:
            if value.get("_id") == target:
                return data_type.from_dict(value)
        return None

    def find(
        self, data_type: type, constraints: dict[str, object]
    ) -> Iterable[_BaseModel]:
        filepath = self.filepath(data_type)
        try:
            filedata = json.loads(filepath.read_text())
        except FileNotFoundError:
            filedata = []
        matches = []
        for value in filedata:
            if constraints == filter_subset(value, constraints.keys()):
                matches.append(value)
        return map(data_type.from_dict, matches)

    def update(
        self, _id: UUID, value: _BaseModel, upsert: bool = False
    ) -> UpdateResult:
        filepath = self.filepath(type(value))
        try:
            filedata = json.loads(filepath.read_text())
        except FileNotFoundError:
            filedata = []
        target = str(_id)
        index = 0
        while index < len(filedata):
            if filedata[index].get("_id") == target:
                new_data = {**value.model_dump(mode="json"), "_id": str(_id)}
                filedata[index] = new_data
                filepath.write_text(json.dumps(filedata))
                return UpdateResult(
                    matched_count=1,
                    did_upsert=False,
                    upserted_id=None
                )
            index += 1
        if upsert:
            return UpdateResult(
                matched_count=0,
                did_upsert=True,
                upserted_id=self.create(value).created_id
            )
        return UpdateResult(
            matched_count=0,
            did_upsert=False,
            upserted_id=None
        )

    def delete(self, data_type: type, _id: UUID) -> DeleteResult:
        filepath = self.filepath(data_type)
        try:
            filedata = json.loads(filepath.read_text())
        except FileNotFoundError:
            filedata = []
        for index, element in enumerate(filedata):
            if element.get("_id") == str(_id):
                filepath.write_text(json.dumps([
                    *filedata[:index], *filedata[index+1:]
                ]))
                return DeleteResult(deleted_count=1)
        return DeleteResult(deleted_count=0)

    def delete_many(self, data_type: type, *_ids: UUID) -> DeleteResult:
        filepath = self.filepath(data_type)
        try:
            filedata = json.loads(filepath.read_text())
        except FileNotFoundError:
            filedata = []
        new_filedata = []
        targets = set(map(str, _ids))
        deleted_count = 0
        for element in filedata:
            if element.get("_id") in targets:
                deleted_count += 1
            else:
                new_filedata.append(element)
        filepath.write_text(json.dumps(new_filedata))
        return DeleteResult(deleted_count=deleted_count)
