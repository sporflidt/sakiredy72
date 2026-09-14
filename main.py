"""API REST de items con FastAPI y MongoDB."""

from contextlib import asynccontextmanager
import re
from typing import Any, AsyncIterator

from bson import ObjectId
from fastapi import FastAPI, HTTPException, Query, Response, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

MONGODB_URI = "mongodb://localhost:27017"
DB_NAME = "bdunab2"
COLL_NAME = "items"

client: AsyncIOMotorClient | None = None
db: Any = None
coll: Any = None


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Abre el cliente de MongoDB al iniciar y lo cierra al apagar la API."""
    global client, db, coll
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    coll = db[COLL_NAME]
    try:
        yield
    finally:
        client.close()
        client = None
        db = None
        coll = None


app = FastAPI(
    title="API de Items",
    version="1.0.0",
    description="CRUD REST de items persistidos en MongoDB.",
    lifespan=lifespan,
)


class Item(BaseModel):
    nombre: str = Field(min_length=1)
    precio: float = Field(gt=0)
    tags: list[str] = Field(default_factory=list)
    activo: bool = True


class ItemIn(Item):
    """Datos que el cliente envía al crear o actualizar un item."""


class ItemOut(Item):
    id: str


def doc_to_itemout(doc: dict[str, Any]) -> ItemOut:
    """Convierte el formato interno de MongoDB al formato público de la API."""
    return ItemOut(
        id=str(doc["_id"]),
        nombre=doc["nombre"],
        precio=doc["precio"],
        tags=doc.get("tags", []),
        activo=doc.get("activo", True),
    )


def get_object_id(item_id: str) -> ObjectId:
    """Valida un id recibido desde una ruta y lo transforma para MongoDB."""
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID invalido")
    return ObjectId(item_id)


def get_collection() -> Any:
    if coll is None:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    return coll


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items", response_model=list[ItemOut])
async def list_items(
    q: str | None = Query(default=None, description="Texto a buscar en el nombre"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[ItemOut]:
    query: dict[str, Any] = {}
    if q:
        # Escapamos el texto para que una búsqueda sea literal y segura.
        query = {"nombre": {"$regex": re.escape(q), "$options": "i"}}

    cursor = get_collection().find(query).skip(skip).limit(limit)
    return [doc_to_itemout(doc) async for doc in cursor]


@app.post("/items", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemIn) -> ItemOut:
    collection = get_collection()
    result = await collection.insert_one(item.model_dump())
    created = await collection.find_one({"_id": result.inserted_id})
    if created is None:
        raise HTTPException(status_code=500, detail="No se pudo recuperar el item creado")
    return doc_to_itemout(created)


@app.get("/items/{item_id}", response_model=ItemOut)
async def get_item(item_id: str) -> ItemOut:
    item = await get_collection().find_one({"_id": get_object_id(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return doc_to_itemout(item)


@app.put("/items/{item_id}", response_model=ItemOut)
async def update_item(item_id: str, item: ItemIn) -> ItemOut:
    collection = get_collection()
    object_id = get_object_id(item_id)
    result = await collection.update_one({"_id": object_id}, {"$set": item.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    updated = await collection.find_one({"_id": object_id})
    if updated is None:
        raise HTTPException(status_code=500, detail="No se pudo recuperar el item actualizado")
    return doc_to_itemout(updated)


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str) -> Response:
    result = await get_collection().delete_one({"_id": get_object_id(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
