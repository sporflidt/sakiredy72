# API REST de items — FastAPI + MongoDB

Implementación del ejercicio de la semana: una API REST asíncrona para crear, consultar, listar, actualizar y eliminar items en MongoDB.

## Requisitos

- Python 3.10 o superior.
- MongoDB ejecutándose localmente en `mongodb://localhost:27017`.

## Instalación y ejecución

```powershell
cd fastapi-mongodb-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

La aplicación usa la base `bdunab2` y la colección `items`. Con MongoDB iniciado, revisa la documentación interactiva en <http://127.0.0.1:8000/docs>.

## Rutas

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Comprueba que la API responde. |
| GET | `/items` | Lista items; acepta `q`, `skip` y `limit`. |
| POST | `/items` | Crea un item. |
| GET | `/items/{item_id}` | Obtiene un item por su id. |
| PUT | `/items/{item_id}` | Reemplaza un item existente. |
| DELETE | `/items/{item_id}` | Elimina un item y responde 204. |

`skip` debe ser 0 o mayor; `limit` está entre 1 y 200. La búsqueda `q` no distingue mayúsculas de minúsculas.

## Ejemplo para crear un item

```json
{
  "nombre": "Teclado",
  "precio": 19990,
  "tags": ["computacion", "perifericos"],
  "activo": true
}
```

Los campos `nombre` y `precio` se validan: el nombre no puede ser vacío y el precio debe ser mayor a cero. Los identificadores con formato incorrecto devuelven 400 y los items inexistentes devuelven 404.
