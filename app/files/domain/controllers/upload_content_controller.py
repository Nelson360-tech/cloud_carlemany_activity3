from app.files.domain.exceptions.file_not_found import FileNotFound
from app.files.domain.exceptions.forbidden import Forbidden
from app.files.domain.persistence.file_persistence_interface import FilePersistenceInterface


class UploadContentController:
    def __init__(self, file_persistence: FilePersistenceInterface):
        self.file_persistence = file_persistence

    async def __call__(self, file_id: int, content: bytes, owner_external_id: int) -> None:
        file = await self.file_persistence.get_by_id(file_id)
        if file is None:
            raise FileNotFound()
        if file.owner_external_id != owner_external_id:
            raise Forbidden()
        await self.file_persistence.update_content(file_id, content)