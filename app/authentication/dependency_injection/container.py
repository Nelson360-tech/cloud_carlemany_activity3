from dependency_injector import containers, providers

from app.authentication.domain.controllers.introspect_controller import IntrospectController
from app.authentication.domain.controllers.login_controller import LoginController
from app.authentication.domain.controllers.logout_controller import LogoutController
from app.authentication.domain.controllers.register_controller import RegisterController
from app.authentication.domain.services.hash_service import HashService
from app.authentication.domain.services.token_service import TokenService
from app.authentication.persistence.session_memory_persistence import SessionMemoryPersistence
from app.authentication.persistence.user_postgres_persistence import UserPostgresPersistence

class Container(containers.DeclarativeContainer):

    # Persistencia
    user_persistence = providers.Singleton(UserPostgresPersistence)
    session_persistence = providers.Singleton(SessionMemoryPersistence)

    # Servicios
    hash_service = providers.Singleton(HashService)
    token_service = providers.Singleton(TokenService)

    # Controladores
    register_controller = providers.Singleton(
        RegisterController,
        user_persistence=user_persistence,
        hash_service=hash_service,
    )

    login_controller = providers.Singleton(
        LoginController,
        user_persistence=user_persistence,
        session_persistence=session_persistence,
        hash_service=hash_service,
        token_service=token_service,
    )

    logout_controller = providers.Singleton(
        LogoutController,
        session_persistence=session_persistence,
    )

    introspect_controller = providers.Singleton(
        IntrospectController,
        session_persistence=session_persistence,
    )