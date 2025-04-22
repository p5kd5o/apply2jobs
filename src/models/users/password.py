from secrets import compare_digest
from typing import Self

from utils.passwords import PasswordHash, hash_password, verify_password

from models.base_model import _BaseModel


# pylint: disable=too-few-public-methods
class Password(_BaseModel):
    digest: str
    salt: str

    @classmethod
    def from_password(cls, password: str | bytes) -> Self:
        password_hash = hash_password(password)
        return cls(
            digest=password_hash.digest.hex(),
            salt=password_hash.salt.hex()
        )

    def __eq__(self, other: Self | PasswordHash | str | bytes) -> bool:
        if isinstance(other, (type(self), PasswordHash)):
            result = (
                compare_digest(bytes.fromhex(self.salt), other.salt) and
                compare_digest(bytes.fromhex(self.digest), other.digest)
            )
        else:
            result = verify_password(
                other,
                PasswordHash(
                    digest=bytes.fromhex(self.digest),
                    salt=bytes.fromhex(self.salt)
                )
            )
        return result
