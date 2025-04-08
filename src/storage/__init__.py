from enum import StrEnum
from typing import Literal

from .base_backend import _BaseBackend
from .filesystem import FilesystemBackend
from .mongodb import MongodbBackend
from .postgresql import PostgresqlBackend


class StorageBackendEnum(StrEnum):
    FILESYSTEM = "filesystem"
    MONGODB = "mongodb"
    POSTGRESQL = "postgresql"


StorageBackend: type = Literal[
    StorageBackendEnum.FILESYSTEM,
    StorageBackendEnum.MONGODB,
    StorageBackendEnum.POSTGRESQL,
]


STORAGE_BACKENDS: dict[str, _BaseBackend] = {
    StorageBackendEnum.FILESYSTEM: FilesystemBackend,
    StorageBackendEnum.MONGODB: MongodbBackend,
    StorageBackendEnum.POSTGRESQL: PostgresqlBackend,
}
