from uuid import UUID
from typing import Any

from bson import objectid
from pydantic_core import core_schema


# pylint: disable=too-few-public-methods
class ObjectId(objectid.ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(objectid.ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                str,
                when_used="json"
            ),
        )

    @classmethod
    def validate(cls, value) -> objectid.ObjectId:
        if not objectid.ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return objectid.ObjectId(value)


_Id = str | UUID | ObjectId
