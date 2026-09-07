import secrets
import itertools

import bcrypt
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

router = APIRouter()

# --- Almacenamiento en memoria ---------------------------------------------
# USERS: key = email, value = {"password_hash": bytes, "external_id": int}
USERS: dict[str, dict] = {}

# SESSIONS: key = token de sesión, value = email del usuario dueño de la sesión
SESSIONS: dict[str, str] = {}

# Contador para generar external_id únicos e incrementales
_id_counter = itertools.count(start=1)


# --- Modelos de entrada -----------------------------------------------------
class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# --- Utilidades internas -----------------------------------------------------
def _hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _verify_password(password: str, password_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash)


def get_current_user_email(auth: str | None) -> str:
    """Valida el token de sesión recibido en el header 'Auth' y devuelve el email asociado."""
    if auth is None or auth not in SESSIONS:
        raise HTTPException(status_code=401, detail="Invalid or missing session token")
    return SESSIONS[auth]


# --- Endpoints ---------------------------------------------------------------
@router.post("/register")
async def register(payload: RegisterRequest) -> dict:
    if payload.email in USERS:
        raise HTTPException(status_code=409, detail="User already exists")

    USERS[payload.email] = {
        "password_hash": _hash_password(payload.password),
        "external_id": next(_id_counter),
    }

    return {"status": "ok", "external_id": USERS[payload.email]["external_id"]}


@router.post("/login")
async def login(payload: LoginRequest) -> dict:
    user = USERS.get(payload.email)
    if user is None or not _verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = secrets.token_hex(32)
    SESSIONS[token] = payload.email

    return {"status": "ok", "token": token}


@router.post("/logout")
async def logout(auth: str | None = Header(default=None)) -> dict:
    if auth is None or auth not in SESSIONS:
        raise HTTPException(status_code=401, detail="Invalid or missing session token")

    del SESSIONS[auth]
    return {"status": "ok"}


@router.get("/introspect")
async def introspect(auth: str | None = Header(default=None)) -> dict:
    email = get_current_user_email(auth)
    user = USERS[email]

    return {
        "status": "ok",
        "email": email,
        "external_id": user["external_id"],
    }