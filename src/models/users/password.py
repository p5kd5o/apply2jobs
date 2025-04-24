from base64 import b64decode, b64encode
from enum import Enum, StrEnum
from secrets import compare_digest
from typing import Annotated, Any, Literal, Optional, Self

from pydantic import BeforeValidator, SerializationInfo, field_serializer

from utils.models import ensure_enum
from utils.passwords import PasswordHash, hash_password, verify_password

from models.base_model import _BaseModel


# pylint: disable=too-few-public-methods
class PasswordEncoding(StrEnum):
    HEX = "hex"
    BASE64 = "base64"


PasswordEncodingType = Literal[
    PasswordEncoding.HEX,
    PasswordEncoding.BASE64,
]
ENCODERS = {
    PasswordEncoding.HEX.value:
    lambda b: b.hex(),
    PasswordEncoding.BASE64.value:
    lambda b: b64encode(b).decode(encoding="utf-8")
}
DECODERS = {
    PasswordEncoding.HEX.value:
    bytes.fromhex,
    PasswordEncoding.BASE64.value:
    lambda s: b64decode(s.encode(encoding="utf-8"))
}


# pylint: disable=too-few-public-methods
class Password(_BaseModel):
    digest: str
    salt: str
    encoding: Optional[Annotated[
        PasswordEncoding,
        BeforeValidator(ensure_enum(PasswordEncoding))
    ]] = PasswordEncoding.HEX

    @field_serializer("encoding")
    def _serialize_enum(self, field_value: Enum, _: SerializationInfo) -> Any:
        return field_value.value

    @classmethod
    def from_password(
        cls,
        password: str | bytes,
        encoding: PasswordEncodingType | str = PasswordEncoding.HEX
    ) -> Self:
        encoding = ensure_enum(PasswordEncoding)(encoding)
        encode = ENCODERS[encoding.value]
        password_hash = hash_password(password)
        return cls(
            digest=encode(password_hash.digest),
            salt=encode(password_hash.salt),
            encoding=encoding
        )

    def __eq__(self, other: Self | PasswordHash | str | bytes) -> bool:
        decode = DECODERS[self.encoding.value]
        if isinstance(other, type(self)):
            decode_other = DECODERS[other.encoding.value]
            return (
                compare_digest(decode(self.salt), decode_other(other.salt)) and
                compare_digest(decode(self.digest), decode_other(other.digest))
            )
        if isinstance(other, PasswordHash):
            return (
                compare_digest(decode(self.salt), other.salt) and
                compare_digest(decode(self.digest), other.digest)
            )
        return verify_password(
            other,
            PasswordHash(digest=decode(self.digest), salt=decode(self.salt))
        )
