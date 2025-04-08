import json
import pathlib
from urllib.parse import unquote, urlparse
from uuid import UUID, uuid4
from typing import Sequence

from models.base_model import _BaseModel
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

    def read_all(self, data_type: type) -> Sequence[_BaseModel]:
        return map(data_type.from_dict, json.loads(
            self.filepath(data_type).read_text()
        ))

    def read(self, _id: UUID, data_type: type) -> _BaseModel | None:
        filepath = self.filepath(data_type)
        try:
            filedata = json.loads(filepath.read_text())
        except FileNotFoundError:
            filedata = []
        for value in filedata:
            if value.get("_id") == str(_id):
                return data_type.from_dict(value)
        return None

    def create(self, data: _BaseModel) -> UUID:
        filepath = self.filepath(type(data))
        try:
            filedata = json.loads(filepath.read_text())
        except FileNotFoundError:
            filedata = []
        new_uuid = uuid4()
        new_data = {**data.model_dump(mode="json"), "_id": str(new_uuid)}
        filepath.write_text(json.dumps([*filedata, new_data]))
        return new_uuid

    def update(
        self, _id: UUID, data: _BaseModel, upsert: bool = False
    ) -> UUID | None:
        filepath = self.filepath(type(data))
        try:
            filedata = json.loads(filepath.read_text())
        except FileNotFoundError:
            filedata = []
        for index, element in enumerate(filedata):
            if element.get("_id") == str(_id):
                new_data = {**data.model_dump(mode="json"), "_id": str(_id)}
                filepath.write_text(json.dumps([
                    *filedata[:index], new_data, *filedata[index+1:]
                ]))
                return _id
        if upsert:
            return self.create(data)
        return None

    def delete(self, _id: UUID, data_type: type) -> UUID | None:
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
                return _id
        return None
