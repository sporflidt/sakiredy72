## Resumen

Implementación de una API REST asíncrona con FastAPI y MongoDB para administrar items.

## Funcionalidades

- Conexión asíncrona a MongoDB y gestión del ciclo de vida de la aplicación.
- Modelos de entrada y salida con validación de nombre, precio, tags y estado.
- Endpoint de salud.
- CRUD completo de items.
- Búsqueda por nombre sin distinguir mayúsculas y paginación.
- Manejo de identificadores inválidos, recursos no encontrados y base de datos no disponible.

## Cómo ejecutar

1. Instalar las dependencias: `python -m pip install -r requirements.txt`.
2. Iniciar MongoDB en `mongodb://localhost:27017`.
3. Ejecutar `python -m uvicorn main:app --reload` desde la carpeta del proyecto.
4. Abrir `/docs` para probar los endpoints.

## Pruebas realizadas

- [x] `GET /health` responde `200`.
- [x] Creación, búsqueda, consulta individual y actualización de un item.
- [x] Eliminación con respuesta `204` y comprobación posterior de `404`.
- [x] ID con formato inválido responde `400`.
- [x] Validación de nombre vacío y precio no positivo responde `422`.
- [x] Valores predeterminados para `tags` y `activo`.
