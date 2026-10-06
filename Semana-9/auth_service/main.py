import os
import secrets
import time
from typing import Optional

from argon2 import PasswordHasher
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from common_secrets import vault_secret

app = FastAPI(title="Al Sahara Auth Service")
ph = PasswordHasher()

AUTH_INTROSPECTION_SECRET = vault_secret("auth_introspection_secret")
SESSION_TTL = 900

USERS = {
    "ana": {
        "user_id": "USR-001",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$vKcSgpE6+6vHHMkkR0fqeg$fvflsYch2k47Bq7y0zfzKYg1YpFiIlaipX+eAMnwmbo",
        "roles": ["user"],
    },
    "ernesto": {
        "user_id": "USR-003",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$W7NvgSffXCHgMjDork9Bjg$xSiBIHNpHYIBGxBiIoLjGY8uajtrnPVgKvbg7SEfmZI",
        "roles": ["user", "admin"],
    },
}

SESSIONS: dict[str, dict] = {}


class Credentials(BaseModel):
    username: str
    password: str


class TokenRequest(BaseModel):
    token: str


def require_gateway_secret(value: Optional[str]) -> None:
    if not value or not secrets.compare_digest(value, AUTH_INTROSPECTION_SECRET):
        raise HTTPException(status_code=403, detail="Gateway no autorizado")


@app.get("/health")
def health():
    return {"status": "ok", "service": "auth"}


@app.post("/login")
def login(credentials: Credentials):
    user = USERS.get(credentials.username)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    try:
        ph.verify(user["password_hash"], credentials.password)
    except Exception:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = secrets.token_urlsafe(32)
    SESSIONS[token] = {
        "user_id": user["user_id"],
        "username": credentials.username,
        "roles": user["roles"],
        "expires_at": time.time() + SESSION_TTL,
    }
    return {"access_token": token, "token_type": "bearer", "expires_in": SESSION_TTL}


@app.post("/introspect")
def introspect(payload: TokenRequest, x_gateway_secret: Optional[str] = Header(default=None)):
    require_gateway_secret(x_gateway_secret)
    session = SESSIONS.get(payload.token)
    if not session or session["expires_at"] <= time.time():
        if session:
            SESSIONS.pop(payload.token, None)
        return {"active": False}

    return {
        "active": True,
        "user_id": session["user_id"],
        "username": session["username"],
        "roles": session["roles"],
    }


@app.post("/logout")
def logout(payload: TokenRequest, x_gateway_secret: Optional[str] = Header(default=None)):
    require_gateway_secret(x_gateway_secret)
    SESSIONS.pop(payload.token, None)
    return {"message": "Sesión revocada"}
