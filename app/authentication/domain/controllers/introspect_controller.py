from app.authentication.domain.bos.user_bo import UserBO
from app.authentication.domain.exceptions.invalid_token import InvalidToken
from app.authentication.domain.persistence.session_persistence_interface import SessionPersistenceInterface


class IntrospectController:
    def __init__(self, session_persistence: SessionPersistenceInterface):
        self.session_persistence = session_persistence

    async def __call__(self, token: str) -> UserBO:
        user = await self.session_persistence.get_user(token)
        if user is None:
            raise InvalidToken()
        return user