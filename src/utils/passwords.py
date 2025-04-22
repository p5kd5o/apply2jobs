from collections import namedtuple
from hashlib import scrypt
from os import urandom
from secrets import compare_digest

N_ITERATIONS = 2048
R_BLOCK_SIZE = 8
P_PARALLELISM = 1
SALT_SIZE = 24

PasswordHash = namedtuple("PasswordHash", ["digest", "salt"])


def hash_password(password: str | bytes) -> tuple[bytes, bytes]:
    if isinstance(password, bytes):
        password_b = password
    else:
        password_b = password.encode("utf-8")
    salt = urandom(SALT_SIZE)
    return PasswordHash(
        digest=scrypt(
            password_b, salt=salt,
            n=N_ITERATIONS, r=R_BLOCK_SIZE, p=P_PARALLELISM
        ),
        salt=salt
    )


def verify_password(
    to_check: str | bytes, password_hash: PasswordHash
) -> bool:
    if isinstance(to_check, bytes):
        to_check_b = to_check
    else:
        to_check_b = to_check.encode("utf-8")
    return compare_digest(
        password_hash.digest,
        scrypt(
            to_check_b, salt=password_hash.salt,
            n=N_ITERATIONS, r=R_BLOCK_SIZE, p=P_PARALLELISM
        )
    )
