from app.authentication.domain.bos.user_bo import UserBO
from app.authentication.domain.persistence.session_persistence_interface import SessionPersistenceInterface


class SessionMemoryPersistence(SessionPersistenceInterface):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._sessions = {}
        return cls._instance

    async def store(self, token: str, user: UserBO) -> None:
        self._sessions[token] = user

    async def get_user(self, token: str) -> UserBO | None:
        return self._sessions.get(token)

    async def delete(self, token: str) -> None:
        self._sessions.pop(token, None)