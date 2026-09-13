from dependency_injector import containers, providers

from app.authentication.persistence.session_memory_persistence import SessionMemoryPersistence
from app.files.domain.controllers.create_file_controller import CreateFileController
from app.files.domain.controllers.delete_file_controller import DeleteFileController
from app.files.domain.controllers.get_file_controller import GetFileController
from app.files.domain.controllers.list_files_controller import ListFilesController
from app.files.domain.controllers.merge_files_controller import MergeFilesController
from app.files.domain.controllers.upload_content_controller import UploadContentController
from app.files.persistence.file_postgres_persistence import FilePostgresPersistence

class Container(containers.DeclarativeContainer):

    file_persistence = providers.Singleton(FilePostgresPersistence)
    session_persistence = providers.Singleton(SessionMemoryPersistence)

    create_file_controller = providers.Singleton(
        CreateFileController,
        file_persistence=file_persistence,
    )

    list_files_controller = providers.Singleton(
        ListFilesController,
        file_persistence=file_persistence,
    )

    get_file_controller = providers.Singleton(
        GetFileController,
        file_persistence=file_persistence,
    )

    delete_file_controller = providers.Singleton(
        DeleteFileController,
        file_persistence=file_persistence,
    )

    upload_content_controller = providers.Singleton(
        UploadContentController,
        file_persistence=file_persistence,
    )

    merge_files_controller = providers.Singleton(
        MergeFilesController,
        file_persistence=file_persistence,
    )