# Al Sahara — Modelo de arquitectura C4

Este directorio contiene la especificación de arquitectura del proyecto Al Sahara en **Structurizr DSL**, junto con diagramas PNG de referencia.

El modelo se construyó exclusivamente a partir de los archivos entregados para esta revisión: `frontend.zip` y `Semana-9.zip`. Los archivos Python independientes `main.py`, `gateway.py` y `backend_api.py` se excluyeron porque fueron identificados como ejercicios o pruebas ajenos al proyecto.

## 1. Alcance y criterio de modelado

El modelo describe el estado implementado en los archivos disponibles. No representa como existentes las funcionalidades que aparecen solo en la interfaz o que estaban planificadas.

### C1 — Contexto

- **Visitante:** navega las páginas públicas del sitio.
- **Consumidor HTTP:** cliente externo o herramienta de pruebas que invoca directamente las API.
- **Plataforma Al Sahara:** sitio web y servicios backend disponibles.
- **HashiCorp Vault:** dependencia externa utilizada para obtener secretos técnicos.

### C2 — Contenedores

| Contenedor | Tecnología | Responsabilidad |
|---|---|---|
| Frontend Web | HTML, CSS, JavaScript | Páginas de inicio, menú, registro y carrito |
| Auth Service | Python 3.11, FastAPI | Login, introspección y revocación de sesiones |
| Backend API | Python 3.11, FastAPI | Consulta de productos y pedidos y eliminación de productos |
| HashiCorp Vault | Vault KV v2 | Almacenamiento de secretos técnicos |

Los puertos 8100 y 9000 son los declarados en la configuración Docker Compose corregida incluida en este paquete. El puerto 8200 corresponde a Vault en el entorno de desarrollo.

**No existe comunicación implementada entre el frontend y las API backend en los archivos revisados.** Por eso no se dibuja una relación entre esos contenedores. El carrito funciona localmente en el navegador.

### C3 — Componentes

**Frontend Web**
- Páginas HTML.
- Catálogo estático definido en HTML.
- Gestor del carrito en JavaScript.
- Persistencia del carrito mediante `localStorage`, bajo la clave `alSaharaCart`.

**Auth Service**
- `GET /health`.
- `POST /login`.
- `POST /introspect`.
- `POST /logout`.
- Usuarios de prueba definidos en el diccionario `USERS`.
- Verificación de contraseñas mediante Argon2id.
- Sesiones en memoria con tokens aleatorios y TTL de 900 segundos.
- Protección de `/introspect` y `/logout` mediante `X-Gateway-Secret`.
- Lectura de `auth_introspection_secret` desde Vault.

**Backend API**
- `GET /health`.
- `GET /products`.
- `GET /orders`.
- `DELETE /products/{product_id}`.
- Productos y pedidos almacenados en listas en memoria (`PRODUCTS` y `ORDERS`).
- Protección de productos y pedidos mediante `X-Gateway-Secret`.
- La eliminación de productos exige además `X-Authenticated-Roles` con el rol `admin`.
- Lectura de `backend_shared_secret` desde Vault.

## 2. Vistas incluidas

- `C1_Contexto`: actores, sistema Al Sahara y Vault.
- `C2_Contenedores`: frontend, Auth Service, Backend API y Vault.
- `C3_Frontend`: componentes del sitio y del carrito.
- `C3_Auth`: componentes internos del servicio de autenticación.
- `C3_Backend`: componentes internos de la API.
- `Dyn_Login`: flujo exitoso de inicio de sesión.
- `Dyn_Introspeccion`: validación de una sesión.
- `Dyn_ConsultaProductos`: consulta protegida del catálogo backend.
- `Dyn_EliminarProducto`: eliminación administrativa de un producto.
- `Dyn_SecretBootstrap`: lectura de secretos al iniciar los servicios.

Los PNG de `diagramas/` son previsualizaciones de referencia. El archivo `workspace.dsl` es la fuente editable del modelo.

## 3. Elementos no modelados como implementados

- **API Gateway:** está declarado en el Compose original, pero no se entregó su código (`backend/gateway/main.py` no existe en el ZIP).
- **GraphQL:** está planificado, pero no está implementado.
- **Pagos:** la página del carrito muestra opciones de pago y un botón de pedido, pero no existe un servicio de pagos ni un flujo backend de compra en los archivos recibidos.
- **Registro:** el formulario HTML no realiza una petición al Auth Service y el servicio no expone un endpoint de registro.
- **Base de datos:** no hay persistencia de usuarios, sesiones, productos o pedidos en una base de datos; esas estructuras están en memoria.
- **Integración frontend-backend:** no se encontraron llamadas `fetch()` desde el frontend a los servicios backend.

## 4. Observaciones de seguridad y límites

1. El Auth Service genera tokens aleatorios de sesión; **no utiliza JWT**.
2. `X-Gateway-Secret` protege endpoints internos, pero el Gateway que debería custodiar y añadir ese secreto no está implementado.
3. `X-Authenticated-Roles` es leído directamente desde un encabezado HTTP. En el código entregado, el Backend API no consulta al Auth Service para comprobar que ese rol provenga de una sesión válida. Por tanto, la comprobación del rol no debe interpretarse como una autorización completa de extremo a extremo.
4. Los secretos de ejemplo y el modo dev de Vault son solo para desarrollo local. No deben usarse en producción.
5. Los datos en memoria se pierden al reiniciar los procesos.

## 5. Visualizar el modelo en Structurizr

1. Abrir [Structurizr Playground](https://playground.structurizr.com/).
2. Copiar el contenido completo de `workspace.dsl` en el editor DSL.
3. Seleccionar las vistas por su identificador: `C1_Contexto`, `C2_Contenedores`, `C3_Frontend`, `C3_Auth`, `C3_Backend` y las vistas `Dyn_*`.
4. Si el Playground muestra un error de DSL, revisar el mensaje del editor; los PNG incluidos sirven como referencia visual, no sustituyen la validación del DSL.

## 6. Configuración Docker corregida incluida

La carpeta `../configuracion-backend-corregida/` contiene una propuesta coherente con la estructura real de `Semana-9.zip`:

- `Dockerfile`: copia `auth_service/`, `backend_api/`, `common_secrets.py` y `requirements.txt` desde las rutas que realmente existen.
- `docker-compose.yml`: levanta Vault, inicializa los secretos y ejecuta Auth Service y Backend API.
- `.env.example`: variables de desarrollo que deben copiarse a `.env`.

El servicio Gateway se omite intencionalmente porque su código no existe. Los endpoints protegidos del Backend API requieren `X-Gateway-Secret`; hasta implementar un Gateway real, las pruebas directas deben hacerse solo en un entorno local controlado.

### Ejecutar el backend corregido

Desde la carpeta `configuracion-backend-corregida/`:

1. Copiar `.env.example` como `.env`.
2. Ejecutar `docker compose up --build`.
3. Auth Service quedará publicado en `http://127.0.0.1:8100`.
4. Backend API quedará publicado en `http://127.0.0.1:9000`.
5. Vault quedará publicado en `http://127.0.0.1:8200`.

La configuración es para desarrollo local. No es una arquitectura de producción y no implementa el Gateway faltante.
