import io
import itertools

from fastapi import APIRouter, HTTPException, Header, UploadFile
from pydantic import BaseModel
from pypdf import PdfReader, PdfWriter

from app.authentication.router import get_current_user_email, USERS

router = APIRouter()

# --- Almacenamiento en memoria ---------------------------------------------
# FILES: key = file id, value = {"owner_external_id": int, "filename": str,
#                                  "description": str, "content": bytes | None}
FILES: dict[int, dict] = {}

_file_id_counter = itertools.count(start=1)


# --- Modelos de entrada -----------------------------------------------------
class CreateFileRequest(BaseModel):
    filename: str
    description: str = ""


class MergeRequest(BaseModel):
    file_id_1: int
    file_id_2: int


# --- Utilidades internas -----------------------------------------------------
def _get_owner_external_id(auth: str | None) -> int:
    email = get_current_user_email(auth)
    return USERS[email]["external_id"]


def _get_owned_file(file_id: int, owner_external_id: int) -> dict:
    file = FILES.get(file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    if file["owner_external_id"] != owner_external_id:
        raise HTTPException(status_code=403, detail="You do not own this file")
    return file


# --- Endpoints ---------------------------------------------------------------
@router.get("")
async def list_files(auth: str | None = Header(default=None)) -> dict:
    owner_id = _get_owner_external_id(auth)

    owned = [
        {
            "id": file_id,
            "filename": file["filename"],
            "description": file["description"],
            "has_content": file["content"] is not None,
        }
        for file_id, file in FILES.items()
        if file["owner_external_id"] == owner_id
    ]

    return {"status": "ok", "files": owned}


@router.post("")
async def create_file(
    payload: CreateFileRequest, auth: str | None = Header(default=None)
) -> dict:
    owner_id = _get_owner_external_id(auth)

    file_id = next(_file_id_counter)
    FILES[file_id] = {
        "owner_external_id": owner_id,
        "filename": payload.filename,
        "description": payload.description,
        "content": None,
    }

    return {"status": "ok", "id": file_id}


# OJO: /merge va ANTES que /{id} porque si no, FastAPI interpreta
# "merge" como si fuera un {id} y nunca llega a esta ruta.
@router.post("/merge")
async def merge_files(
    payload: MergeRequest, auth: str | None = Header(default=None)
) -> dict:
    owner_id = _get_owner_external_id(auth)

    file_1 = _get_owned_file(payload.file_id_1, owner_id)
    file_2 = _get_owned_file(payload.file_id_2, owner_id)

    if file_1["content"] is None or file_2["content"] is None:
        raise HTTPException(
            status_code=400, detail="Both files must have content uploaded before merging"
        )

    writer = PdfWriter()
    for content in (file_1["content"], file_2["content"]):
        reader = PdfReader(io.BytesIO(content))
        for page in reader.pages:
            writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    merged_content = output.getvalue()

    merged_id = next(_file_id_counter)
    FILES[merged_id] = {
        "owner_external_id": owner_id,
        "filename": f"merged_{file_1['filename']}_{file_2['filename']}.pdf",
        "description": "Merged file",
        "content": merged_content,
    }

    return {"status": "ok", "id": merged_id}


@router.get("/{id}")
async def get_file(id: int, auth: str | None = Header(default=None)) -> dict:
    owner_id = _get_owner_external_id(auth)
    file = _get_owned_file(id, owner_id)

    return {
        "status": "ok",
        "id": id,
        "filename": file["filename"],
        "description": file["description"],
        "has_content": file["content"] is not None,
    }


@router.delete("/{id}")
async def delete_file(id: int, auth: str | None = Header(default=None)) -> dict:
    owner_id = _get_owner_external_id(auth)
    _get_owned_file(id, owner_id)

    del FILES[id]
    return {"status": "ok"}


@router.post("/{id}")
async def upload_file_content(
    id: int, file: UploadFile, auth: str | None = Header(default=None)
) -> dict:
    owner_id = _get_owner_external_id(auth)
    owned_file = _get_owned_file(id, owner_id)

    content = await file.read()
    owned_file["content"] = content

    return {"status": "ok"}