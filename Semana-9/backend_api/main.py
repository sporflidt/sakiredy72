import os
import secrets
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException

from common_secrets import vault_secret

app = FastAPI(title="Protected Backend API")

INTERNAL_GATEWAY_SECRET = vault_secret("backend_shared_secret")

PRODUCTS = [
    {"id": 1, "name": "Notebook", "price": 900000},
    {"id": 2, "name": "Monitor", "price": 250000},
]

ORDERS = [
    {"id": 1001, "status": "paid"},
    {"id": 1002, "status": "pending"},
]


def verify_gateway(x_gateway_secret: str = Header(default="")):
    if not secrets.compare_digest(x_gateway_secret, INTERNAL_GATEWAY_SECRET):
        raise HTTPException(status_code=403, detail="Solicitud no autorizada desde Gateway")


def require_admin(x_authenticated_roles: str = Header(default="")):
    roles = {role.strip() for role in x_authenticated_roles.split(",") if role.strip()}
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Se requiere rol admin")


@app.get("/health")
def health():
    return {"status": "OK", "service": "backend"}


@app.get("/products", dependencies=[Depends(verify_gateway)])
def products(x_authenticated_client: Optional[str] = Header(default=None)):
    return {
        "authenticated_client": x_authenticated_client,
        "products": PRODUCTS,
    }


@app.get("/orders", dependencies=[Depends(verify_gateway)])
def orders(
    x_authenticated_client: Optional[str] = Header(default=None),
    x_authenticated_user: Optional[str] = Header(default=None),
):
    return {
        "authenticated_client": x_authenticated_client,
        "authenticated_user": x_authenticated_user,
        "orders": ORDERS,
    }


@app.delete(
    "/products/{product_id}",
    dependencies=[Depends(verify_gateway), Depends(require_admin)],
)
def delete_product(product_id: int):
    for index, product in enumerate(PRODUCTS):
        if product["id"] == product_id:
            deleted = PRODUCTS.pop(index)
            return {"message": "Producto eliminado", "product": deleted}

    raise HTTPException(status_code=404, detail="Producto no encontrado")
