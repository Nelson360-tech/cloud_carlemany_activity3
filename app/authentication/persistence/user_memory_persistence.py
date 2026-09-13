from app.authentication.domain.bos.user_bo import UserBO
from app.authentication.domain.persistence.user_persistence_interface import UserPersistenceInterface


class UserMemoryPersistence(UserPersistenceInterface):

    def __init__(self):
        self._users: dict[str, UserBO] = {}
        self._next_id: int = 1

    async def exists(self, email: str) -> bool:
        return email in self._users

    async def store(self, user: UserBO) -> UserBO:
        user.external_id = self._next_id
        self._next_id += 1
        self._users[user.email] = user
        return user

    async def get_by_email(self, email: str) -> UserBO | None:
        return self._users.get(email)