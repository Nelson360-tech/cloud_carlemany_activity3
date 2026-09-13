from app.authentication.domain.bos.user_bo import UserBO
from app.authentication.domain.exceptions.user_already_exists import UserAlreadyExists
from app.authentication.domain.persistence.user_persistence_interface import UserPersistenceInterface
from app.authentication.domain.services.hash_service import HashService


class RegisterController:
    def __init__(self, user_persistence: UserPersistenceInterface, hash_service: HashService):
        self.user_persistence = user_persistence
        self.hash_service = hash_service

    async def __call__(self, email: str, password: str) -> UserBO:
        if await self.user_persistence.exists(email):
            raise UserAlreadyExists()

        hashed = self.hash_service(password)
        user = UserBO(email=email, password=hashed)
        return await self.user_persistence.store(user)