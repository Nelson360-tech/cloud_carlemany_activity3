from app.files.domain.bos.file_bo import FileBO
from app.files.domain.persistence.file_persistence_interface import FilePersistenceInterface


class ListFilesController:
    def __init__(self, file_persistence: FilePersistenceInterface):
        self.file_persistence = file_persistence

    async def __call__(self, owner_external_id: int) -> list[FileBO]:
        return await self.file_persistence.list_by_owner(owner_external_id)