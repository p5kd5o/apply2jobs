from secrets import compare_digest
from typing import Self

from models.base_model import _BaseModel
from utils.passwords import PasswordHash, hash_password, verify_password


# pylint: disable=too-few-public-methods
class Password(_BaseModel):
    digest: bytes
    salt: bytes

    @classmethod
    def from_password(cls, password: str | bytes) -> Self:
        password_hash = hash_password(password)
        return cls(digest=password_hash.digest, salt=password_hash.salt)

    def __eq__(self, other: Self | PasswordHash | str | bytes) -> bool:
        if isinstance(other, (type(self), PasswordHash)):
            result = (
                compare_digest(self.salt, other.salt) and
                compare_digest(self.digest, other.digest)
            )
        else:
            result = verify_password(
                other, PasswordHash(digest=self.digest, salt=self.salt)
            )
        return result
