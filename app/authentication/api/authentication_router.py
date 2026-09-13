from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from app.authentication.dependency_injection.container import Container
from app.authentication.domain.exceptions.invalid_credentials import InvalidCredentials
from app.authentication.domain.exceptions.invalid_token import InvalidToken
from app.authentication.domain.exceptions.user_already_exists import UserAlreadyExists

router = APIRouter()
container = Container()


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(payload: RegisterRequest) -> dict:
    try:
        user = await container.register_controller()(payload.email, payload.password)
    except UserAlreadyExists:
        raise HTTPException(status_code=409, detail="User already exists")
    return {"status": "ok", "external_id": user.external_id}


@router.post("/login")
async def login(payload: LoginRequest) -> dict:
    try:
        token = await container.login_controller()(payload.email, payload.password)
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"status": "ok", "token": token}


@router.post("/logout")
async def logout(auth: str | None = Header(default=None)) -> dict:
    if auth is None:
        raise HTTPException(status_code=401, detail="Invalid or missing session token")
    try:
        await container.logout_controller()(auth)
    except InvalidToken:
        raise HTTPException(status_code=401, detail="Invalid or missing session token")
    return {"status": "ok"}


@router.get("/introspect")
async def introspect(auth: str | None = Header(default=None)) -> dict:
    if auth is None:
        raise HTTPException(status_code=401, detail="Invalid or missing session token")
    try:
        user = await container.introspect_controller()(auth)
    except InvalidToken:
        raise HTTPException(status_code=401, detail="Invalid or missing session token")
    return {"status": "ok", "email": user.email, "external_id": user.external_id}