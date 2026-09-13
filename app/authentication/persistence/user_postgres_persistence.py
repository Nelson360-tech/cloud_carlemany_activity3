from app.authentication.domain.bos.user_bo import UserBO
from app.authentication.domain.persistence.user_persistence_interface import UserPersistenceInterface
from app.authentication.models import User


class UserPostgresPersistence(UserPersistenceInterface):

    async def exists(self, email: str) -> bool:
        return await User.exists(email=email)

    async def store(self, user: UserBO) -> UserBO:
        db_user = await User.create(
            email=user.email,
            password=user.password,
        )
        return UserBO(
            email=db_user.email,
            password=db_user.password,
            external_id=db_user.id,
        )

    async def get_by_email(self, email: str) -> UserBO | None:
        db_user = await User.get_or_none(email=email)
        if db_user is None:
            return None
        return UserBO(
            email=db_user.email,
            password=db_user.password,
            external_id=db_user.id,
        )