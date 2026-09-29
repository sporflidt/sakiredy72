# Laboratorio: API Gateway local con FastAPI y HashiCorp Vault

Paquete de apoyo basado en la guía PDF adjunta. Incluye el backend protegido, el Gateway seguro, dependencias y pasos para ejecutar las pruebas.

## Arquitectura

- HOST A: API Gateway (`:8000`) y Vault (`:8200`)
- HOST B: API de negocio (`:9000`)
- El cliente presenta un Bearer Token al Gateway.
- El Gateway consulta Vault, valida el token y reenvía la solicitud con una credencial interna al backend.

Las IP `192.168.1.10` y `192.168.1.20` son ejemplos. Sustitúyelas por las IP reales de tus equipos.

> **Solo laboratorio:** Vault se inicia en modo desarrollo con un token raíz de prueba. No uses esta configuración en producción.

## 1. Preparar HOST B (backend)

Abre PowerShell en esta carpeta, entra a `backend` y crea el entorno:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:INTERNAL_GATEWAY_SECRET="gateway-api-secret-456"
uvicorn backend_api:app --host 0.0.0.0 --port 9000
```

Deja esta terminal abierta. La variable de entorno debe llamarse exactamente `INTERNAL_GATEWAY_SECRET`, como la usa el código de este paquete y la guía.

## 2. Preparar HOST A (Vault y Gateway)

En HOST A, copia la carpeta `gateway` y abre PowerShell dentro de ella. Instala las dependencias:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Inicia Vault con Docker (si aún no existe el contenedor):

```powershell
docker run --name vault-dev -p 8200:8200 -e VAULT_DEV_ROOT_TOKEN_ID=dev-only-token -d hashicorp/vault
```

Guarda las credenciales de prueba en Vault:

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv put secret/gateway client_token="student-token-123" backend_shared_secret="gateway-api-secret-456"
```

Configura el Gateway en la misma terminal donde lo ejecutarás:

```powershell
$env:VAULT_ADDR="http://127.0.0.1:8200"
$env:VAULT_TOKEN="dev-only-token"
$env:BACKEND_URL="http://192.168.1.20:9000"
```

Cambia `192.168.1.20` por la IP real de HOST B. Luego inicia:

```powershell
uvicorn gateway:app --host 0.0.0.0 --port 8000
```

## 3. Pruebas (desde HOST A)

Sin token: debe responder `401`.

```powershell
curl.exe -i http://localhost:8000/api/products
```

Token incorrecto: debe responder `401`.

```powershell
curl.exe -i -H "Authorization: Bearer token-incorrecto" http://localhost:8000/api/products
```

Token válido: debe responder `200` con productos.

```powershell
curl.exe -i -H "Authorization: Bearer student-token-123" http://localhost:8000/api/products
```

Pedidos:

```powershell
curl.exe -i -H "Authorization: Bearer student-token-123" http://localhost:8000/api/orders
```

## 4. Prueba de acceso directo al backend (HOST B)

Sin secreto interno, debe responder `403`:

```powershell
curl.exe -i http://localhost:9000/products
```

Con el secreto correcto, debe responder `200`:

```powershell
curl.exe -i -H "X-Gateway-Secret: gateway-api-secret-456" http://localhost:9000/products
```

## 5. Rotación del token

Actualiza el token en Vault sin cambiar el código:

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv put secret/gateway client_token="nuevo-token-789" backend_shared_secret="gateway-api-secret-456"
```

El token antiguo debe devolver `401`; el nuevo debe devolver `200`:

```powershell
curl.exe -i -H "Authorization: Bearer nuevo-token-789" http://localhost:8000/api/products
```

El Gateway consulta Vault por solicitud protegida, por lo que no requiere reinicio para leer el valor nuevo.

## 6. Códigos esperados

| Escenario | HTTP |
|---|---:|
| Falta el Bearer Token | 401 |
| Token incorrecto | 401 |
| Token válido y solicitud correcta | 200 |
| Acceso directo al backend sin secreto | 403 |
| Vault no disponible o no permite consultar | 500 |
| Backend no disponible | 502 |

## Nota sobre el nombre del secreto

Si tu proyecto anterior muestra el error `Falta configurar GATEWAY_SECRET`, revisa que el nombre que lee tu archivo sea el mismo que configuras en PowerShell. Este paquete usa `INTERNAL_GATEWAY_SECRET` en el backend, que es el nombre de la guía PDF. No configures ambas variables a ciegas: mantén un solo nombre consistente entre código y terminal.
