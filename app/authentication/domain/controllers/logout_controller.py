from app.authentication.domain.exceptions.invalid_token import InvalidToken
from app.authentication.domain.persistence.session_persistence_interface import SessionPersistenceInterface


class LogoutController:
    def __init__(self, session_persistence: SessionPersistenceInterface):
        self.session_persistence = session_persistence

    async def __call__(self, token: str) -> None:
        user = await self.session_persistence.get_user(token)
        if user is None:
            raise InvalidToken()
        await self.session_persistence.delete(token)