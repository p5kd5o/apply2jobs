from dataclasses import dataclass

from utils.types import _Id


@dataclass
class CreateOneResult:
    created_id: _Id


@dataclass
class CreateManyResult:
    created_count: int
    created_ids: list[_Id]


@dataclass
class UpdateResult:
    matched_count: int
    did_upsert: bool
    upserted_id: _Id | None = None


@dataclass
class DeleteResult:
    deleted_count: int
