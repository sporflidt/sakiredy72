import os
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from common_secrets import vault_secret

app = FastAPI(
    title="Secure Local API Gateway",
    description="API Gateway con Vault, sesiones y proxy al Backend",
)

AUTH_URL = os.getenv("AUTH_URL", "http://127.0.0.1:8100")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:9000")
BACKEND_SHARED_SECRET = vault_secret("backend_shared_secret")
AUTH_INTROSPECTION_SECRET = vault_secret("auth_introspection_secret")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5500")
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "public"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class LoginPayload(BaseModel):
    username: str
    password: str


async def introspect(token: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{AUTH_URL}/introspect",
                json={"token": token},
                headers={"X-Gateway-Secret": AUTH_INTROSPECTION_SECRET},
            )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Auth Service no disponible")

    if response.status_code == 403:
        raise HTTPException(status_code=503, detail="No se pudo validar la sesión")
    if response.status_code != 200:
        raise HTTPException(status_code=503, detail="No se pudo validar la sesión")

    return response.json()


async def require_session(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=401, detail="Sesión no iniciada")

    identity = await introspect(token)
    if not identity.get("active"):
        raise HTTPException(status_code=401, detail="Sesión inválida o expirada")

    return token, identity


@app.get("/health")
def health():
    return {"status": "OK", "service": "API Gateway"}


@app.post("/auth/login")
async def login(payload: LoginPayload, response: Response):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            auth_response = await client.post(f"{AUTH_URL}/login", json=payload.model_dump())
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Auth Service no disponible")

    if auth_response.status_code == 401:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    if auth_response.status_code != 200:
        raise HTTPException(status_code=502, detail="Respuesta inválida del Auth Service")

    data = auth_response.json()
    token = data["access_token"]
    max_age = int(data.get("expires_in", 900))

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        max_age=max_age,
        path="/",
    )

    return {"message": "Login correcto"}


@app.get("/auth/me")
async def me(request: Request):
    _, identity = await require_session(request)
    return identity


@app.post("/auth/logout")
async def logout(request: Request, response: Response):
    token, _ = await require_session(request)

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            auth_response = await client.post(
                f"{AUTH_URL}/logout",
                json={"token": token},
                headers={"X-Gateway-Secret": AUTH_INTROSPECTION_SECRET},
            )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Auth Service no disponible")

    if auth_response.status_code != 200:
        raise HTTPException(status_code=502, detail="No se pudo cerrar la sesión")

    response.delete_cookie("session_token", path="/")
    return {"message": "Logout correcto"}


async def backend_request(method: str, path: str, identity: dict):
    gateway_headers = {
        "X-Gateway-Secret": BACKEND_SHARED_SECRET,
        "X-Authenticated-Client": "student-client",
        "X-Authenticated-User": identity["user_id"],
        "X-Authenticated-Username": identity["username"],
        "X-Authenticated-Roles": ",".join(identity["roles"]),
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            upstream = await client.request(
                method,
                f"{BACKEND_URL.rstrip('/')}{path}",
                headers=gateway_headers,
            )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Backend no disponible")

    if upstream.status_code >= 500:
        raise HTTPException(status_code=502, detail="Error del Backend")

    return upstream


def proxy_response(upstream: httpx.Response) -> Response:
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        media_type=upstream.headers.get("content-type", "application/json"),
    )


@app.get("/api/products")
async def api_products(request: Request):
    _, identity = await require_session(request)
    return proxy_response(await backend_request("GET", "/products", identity))


@app.get("/api/orders")
async def api_orders(request: Request):
    _, identity = await require_session(request)
    return proxy_response(await backend_request("GET", "/orders", identity))


@app.delete("/api/products/{product_id}")
async def api_delete_product(product_id: int, request: Request):
    _, identity = await require_session(request)

    if "admin" not in identity.get("roles", []):
        raise HTTPException(status_code=403, detail="Se requiere rol admin")

    return proxy_response(
        await backend_request("DELETE", f"/products/{product_id}", identity)
    )


# El Gateway puede servir el Frontend para reproducir la arquitectura de la guía:
# Gateway + Frontend en :8000. El montaje se declara al final para no capturar
# las rutas /auth, /api y /health.
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
