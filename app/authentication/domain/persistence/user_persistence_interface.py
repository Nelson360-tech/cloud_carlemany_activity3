
from abc import ABC, abstractmethod

from app.authentication.domain.bos.user_bo import UserBO


class UserPersistenceInterface(ABC):

    @abstractmethod
    async def exists(self, email: str) -> bool:
        pass

    @abstractmethod
    async def store(self, user: UserBO) -> UserBO:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserBO | None:
        pass