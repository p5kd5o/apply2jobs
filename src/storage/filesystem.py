import json
import pathlib
from urllib.parse import unquote, urlparse
from uuid import UUID, uuid4
from typing import Sequence

from models.base_model import _BaseModel
from utils.mappings import filter_subset
from utils.sortedlist import SortedList
from utils.strcase import CasedStr, CaseType
from .base_backend import _BaseBackend


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

    def create(self, value: _BaseModel) -> UUID:
        filepath = self.filepath(type(value))
        try:
            filedata = SortedList(
                json.loads(filepath.read_text()),
                key=lambda x: x["_id"]
            )
        except FileNotFoundError:
            filedata = SortedList(
                key=lambda x: x["_id"]
            )
        new_uuid = uuid4()
        new_data = {**value.model_dump(mode="json"), "_id": str(new_uuid)}
        filedata.append(new_data)
        filepath.write_text(json.dumps(filedata))
        return new_uuid

    def create_many(self, data_type: type, *values: _BaseModel) -> list[UUID]:
        filepath = self.filepath(data_type)
        try:
            filedata = SortedList(
                json.loads(filepath.read_text()),
                key=lambda x: x["_id"]
            )
        except FileNotFoundError:
            filedata = SortedList(
                key=lambda x: x["_id"]
            )
        uuids = []
        for value in values:
            new_uuid = uuid4()
            new_data = {**value.model_dump(mode="json"), "_id": str(new_uuid)}
            uuids.append(new_uuid)
            filedata.append(new_data)
        filepath.write_text(json.dumps(filedata))
        return uuids

    def get(self, data_type: type, _id: UUID) -> _BaseModel | None:
        filepath = self.filepath(data_type)
        try:
            filedata = SortedList(
                json.loads(filepath.read_text()),
                key=lambda x: x["_id"]
            )
        except FileNotFoundError:
            filedata = SortedList(
                key=lambda x: x["_id"]
            )
        try:
            return data_type.from_dict(filedata[filedata.index(str(_id))])
        except ValueError:
            return None

    def find(
        self, data_type: type, constraints: dict[str, object]
    ) -> Sequence[_BaseModel]:
        filepath = self.filepath(data_type)
        try:
            filedata = SortedList(
                json.loads(filepath.read_text()),
                key=lambda x: x["_id"]
            )
        except FileNotFoundError:
            filedata = SortedList(
                key=lambda x: x["_id"]
            )
        matches = []
        for value in filedata:
            if constraints == filter_subset(value, constraints.keys()):
                matches.append(value)
        return map(data_type.from_dict, matches)

    def update(
        self, _id: UUID, value: _BaseModel, upsert: bool = False
    ) -> UUID | None:
        filepath = self.filepath(type(value))
        try:
            filedata = SortedList(
                json.loads(filepath.read_text()),
                key=lambda x: x["_id"]
            )
        except FileNotFoundError:
            filedata = SortedList(
                key=lambda x: x["_id"]
            )
        try:
            del filedata[filedata.index(str(_id))]
        except ValueError:
            return self.create(value) if upsert else None
        new_data = {**value.model_dump(mode="json"), "_id": str(_id)}
        filedata.append(new_data)
        filepath.write_text(json.dumps(filedata))
        return _id

    def delete(self, data_type: type, _id: UUID) -> UUID | None:
        filepath = self.filepath(data_type)
        try:
            filedata = SortedList(
                json.loads(filepath.read_text()),
                key=lambda x: x["_id"]
            )
        except FileNotFoundError:
            filedata = SortedList(
                key=lambda x: x["_id"]
            )
        try:
            del filedata[filedata.index(str(_id))]
        except ValueError:
            return None
        filepath.write_text(json.dumps(filedata))
        return _id

    def delete_many(self, data_type: type, *_ids: UUID) -> list[UUID]:
        filepath = self.filepath(data_type)
        try:
            filedata = SortedList(
                json.loads(filepath.read_text()),
                key=lambda x: x["_id"]
            )
        except FileNotFoundError:
            filedata = SortedList(
                key=lambda x: x["_id"]
            )
        deleted = []
        for _id in _ids:
            try:
                del filedata[filedata.index(str(_id))]
            except ValueError:
                pass
            else:
                deleted.append(_id)
        filepath.write_text(json.dumps(filedata))
        return deleted
