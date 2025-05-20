from logging import getLogger
from typing import Iterator

from models import User
from utils.types import _Id

from services.base_service import _BaseService

LOGGER = getLogger(__name__)


class UsersService(_BaseService):

    def find_users(self, **constraints) -> Iterator[User]:
        return self.backend.find(User, constraints)

    def create_user(self, user: User) -> _Id | None:
        try:
            next(self.find_users(username=user.username))
        except StopIteration:
            pass
        else:
            return None

        try:
            next(self.find_users(email_address=user.email_address))
        except StopIteration:
            pass
        else:
            return None

        return self.backend.create(user).created_id
