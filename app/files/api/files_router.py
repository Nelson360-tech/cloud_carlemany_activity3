from fastapi import APIRouter, Header, HTTPException, UploadFile
from pydantic import BaseModel

from app.authentication.persistence.session_memory_persistence import SessionMemoryPersistence
from app.files.dependency_injection.container import Container
from app.files.domain.exceptions.file_not_found import FileNotFound
from app.files.domain.exceptions.forbidden import Forbidden

router = APIRouter()
container = Container()


class CreateFileRequest(BaseModel):
    filename: str
    description: str = ""


class MergeRequest(BaseModel):
    file_id_1: int
    file_id_2: int


async def _get_owner_external_id(auth: str | None) -> int:
    if auth is None:
        raise HTTPException(status_code=401, detail="Invalid or missing session token")
    sessions = SessionMemoryPersistence()
    user = await sessions.get_user(auth)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or missing session token")
    return user.external_id


@router.get("")
async def list_files(auth: str | None = Header(default=None)) -> dict:
    owner_id = await _get_owner_external_id(auth)
    files = await container.list_files_controller()(owner_id)
    return {
        "status": "ok",
        "files": [
            {"id": f.id, "filename": f.filename, "description": f.description, "has_content": f.content is not None}
            for f in files
        ],
    }


@router.post("")
async def create_file(payload: CreateFileRequest, auth: str | None = Header(default=None)) -> dict:
    owner_id = await _get_owner_external_id(auth)
    file = await container.create_file_controller()(payload.filename, payload.description, owner_id)
    return {"status": "ok", "id": file.id}


@router.post("/merge")
async def merge_files(payload: MergeRequest, auth: str | None = Header(default=None)) -> dict:
    owner_id = await _get_owner_external_id(auth)
    try:
        merged = await container.merge_files_controller()(payload.file_id_1, payload.file_id_2, owner_id)
    except FileNotFound:
        raise HTTPException(status_code=404, detail="File not found")
    except Forbidden:
        raise HTTPException(status_code=403, detail="You do not own this file")
    return {"status": "ok", "id": merged.id}


@router.get("/{id}")
async def get_file(id: int, auth: str | None = Header(default=None)) -> dict:
    owner_id = await _get_owner_external_id(auth)
    try:
        file = await container.get_file_controller()(id, owner_id)
    except FileNotFound:
        raise HTTPException(status_code=404, detail="File not found")
    except Forbidden:
        raise HTTPException(status_code=403, detail="You do not own this file")
    return {
        "status": "ok",
        "id": file.id,
        "filename": file.filename,
        "description": file.description,
        "has_content": file.content is not None,
    }


@router.delete("/{id}")
async def delete_file(id: int, auth: str | None = Header(default=None)) -> dict:
    owner_id = await _get_owner_external_id(auth)
    try:
        await container.delete_file_controller()(id, owner_id)
    except FileNotFound:
        raise HTTPException(status_code=404, detail="File not found")
    except Forbidden:
        raise HTTPException(status_code=403, detail="You do not own this file")
    return {"status": "ok"}


@router.post("/{id}")
async def upload_content(id: int, file: UploadFile, auth: str | None = Header(default=None)) -> dict:
    owner_id = await _get_owner_external_id(auth)
    content = await file.read()
    try:
        await container.upload_content_controller()(id, content, owner_id)
    except FileNotFound:
        raise HTTPException(status_code=404, detail="File not found")
    except Forbidden:
        raise HTTPException(status_code=403, detail="You do not own this file")
    return {"status": "ok"}