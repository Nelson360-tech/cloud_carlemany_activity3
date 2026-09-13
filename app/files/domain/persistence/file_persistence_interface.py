from abc import ABC, abstractmethod

from app.files.domain.bos.file_bo import FileBO


class FilePersistenceInterface(ABC):

    @abstractmethod
    async def store(self, file: FileBO) -> FileBO:
        pass

    @abstractmethod
    async def get_by_id(self, file_id: int) -> FileBO | None:
        pass

    @abstractmethod
    async def list_by_owner(self, owner_external_id: int) -> list[FileBO]:
        pass

    @abstractmethod
    async def delete(self, file_id: int) -> None:
        pass

    @abstractmethod
    async def update_content(self, file_id: int, content: bytes) -> None:
        pass