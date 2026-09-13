import io

from pypdf import PdfReader, PdfWriter

from app.files.domain.bos.file_bo import FileBO
from app.files.domain.exceptions.file_not_found import FileNotFound
from app.files.domain.exceptions.forbidden import Forbidden
from app.files.domain.persistence.file_persistence_interface import FilePersistenceInterface


class MergeFilesController:
    def __init__(self, file_persistence: FilePersistenceInterface):
        self.file_persistence = file_persistence

    async def __call__(self, file_id_1: int, file_id_2: int, owner_external_id: int) -> FileBO:
        f1 = await self.file_persistence.get_by_id(file_id_1)
        f2 = await self.file_persistence.get_by_id(file_id_2)

        if f1 is None or f2 is None:
            raise FileNotFound()
        if f1.owner_external_id != owner_external_id or f2.owner_external_id != owner_external_id:
            raise Forbidden()
        if f1.content is None or f2.content is None:
            raise FileNotFound()

        writer = PdfWriter()
        for content in (f1.content, f2.content):
            reader = PdfReader(io.BytesIO(content))
            for page in reader.pages:
                writer.add_page(page)

        output = io.BytesIO()
        writer.write(output)

        merged = FileBO(
            filename=f"merged_{f1.filename}_{f2.filename}.pdf",
            description="Merged file",
            owner_external_id=owner_external_id,
            content=output.getvalue(),
        )
        return await self.file_persistence.store(merged)