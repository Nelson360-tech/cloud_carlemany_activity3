from app.files.domain.bos.file_bo import FileBO
from app.files.domain.persistence.file_persistence_interface import FilePersistenceInterface
from app.files.models import File


class FilePostgresPersistence(FilePersistenceInterface):

    async def store(self, file: FileBO) -> FileBO:
        db_file = await File.create(
            owner_id=file.owner_external_id,
            filename=file.filename,
            description=file.description,
            content=file.content,
        )
        return FileBO(
            filename=db_file.filename,
            description=db_file.description,
            owner_external_id=db_file.owner_id,
            content=db_file.content,
            id=db_file.id,
        )

    async def get_by_id(self, file_id: int) -> FileBO | None:
        db_file = await File.get_or_none(id=file_id)
        if db_file is None:
            return None
        return FileBO(
            filename=db_file.filename,
            description=db_file.description,
            owner_external_id=db_file.owner_id,
            content=db_file.content,
            id=db_file.id,
        )

    async def list_by_owner(self, owner_external_id: int) -> list[FileBO]:
        db_files = await File.filter(owner_id=owner_external_id)
        return [
            FileBO(
                filename=f.filename,
                description=f.description,
                owner_external_id=f.owner_id,
                content=f.content,
                id=f.id,
            )
            for f in db_files
        ]

    async def delete(self, file_id: int) -> None:
        await File.filter(id=file_id).delete()

    async def update_content(self, file_id: int, content: bytes) -> None:
        await File.filter(id=file_id).update(content=content)