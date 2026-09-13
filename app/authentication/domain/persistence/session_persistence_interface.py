from abc import ABC, abstractmethod

from app.authentication.domain.bos.user_bo import UserBO


class SessionPersistenceInterface(ABC):

    @abstractmethod
    async def store(self, token: str, user: UserBO) -> None:
        pass

    @abstractmethod
    async def get_user(self, token: str) -> UserBO | None:
        pass

    @abstractmethod
    async def delete(self, token: str) -> None:
        pass