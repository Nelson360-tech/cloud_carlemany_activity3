from app.authentication.domain.exceptions.invalid_credentials import InvalidCredentials
from app.authentication.domain.persistence.session_persistence_interface import SessionPersistenceInterface
from app.authentication.domain.persistence.user_persistence_interface import UserPersistenceInterface
from app.authentication.domain.services.hash_service import HashService
from app.authentication.domain.services.token_service import TokenService


class LoginController:
    def __init__(
        self,
        user_persistence: UserPersistenceInterface,
        session_persistence: SessionPersistenceInterface,
        hash_service: HashService,
        token_service: TokenService,
    ):
        self.user_persistence = user_persistence
        self.session_persistence = session_persistence
        self.hash_service = hash_service
        self.token_service = token_service

    async def __call__(self, email: str, password: str) -> str:
        user = await self.user_persistence.get_by_email(email)
        if user is None or not self.hash_service.verify(password, user.password):
            raise InvalidCredentials()

        token = self.token_service()
        await self.session_persistence.store(token, user)
        return token