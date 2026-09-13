from app.files.domain.bos.file_bo import FileBO
from app.files.domain.persistence.file_persistence_interface import FilePersistenceInterface


class CreateFileController:
    def __init__(self, file_persistence: FilePersistenceInterface):
        self.file_persistence = file_persistence

    async def __call__(self, filename: str, description: str, owner_external_id: int) -> FileBO:
        file = FileBO(
            filename=filename,
            description=description,
            owner_external_id=owner_external_id,
        )
        return await self.file_persistence.store(file)