# Observaciones de implementación — Al Sahara

## Confirmado en los archivos recibidos

- Frontend estático: `index.html`, `menu.html`, `registro.html`, `carrito.html`, CSS, imágenes y `js/script.js`.
- El carrito usa `localStorage` con la clave `alSaharaCart`.
- El menú define productos y precios en HTML.
- El formulario de registro no contiene una integración con el Auth Service.
- Auth Service usa Argon2id, tokens aleatorios y sesiones en memoria.
- El TTL de sesión es 900 segundos.
- Auth Service protege `/introspect` y `/logout` con `X-Gateway-Secret`.
- Backend API mantiene `PRODUCTS` y `ORDERS` en memoria.
- Backend API protege `/products` y `/orders` con `X-Gateway-Secret`.
- DELETE `/products/{product_id}` requiere además que `X-Authenticated-Roles` contenga `admin`.
- Los secretos se cargan mediante `common_secrets.vault_secret` desde Vault KV v2.

## No confirmado / no implementado en el material

- Código del API Gateway.
- GraphQL.
- API de pagos y procesamiento de órdenes desde el carrito.
- Conexión HTTP desde frontend hacia backend.
- Persistencia en base de datos.
- Registro de usuarios desde el formulario.

## Riesgo de autorización

El Backend API acepta `X-Authenticated-Roles` como encabezado sin verificar por sí mismo el token de sesión en Auth Service. La arquitectura prevista podría delegar esa validación a un Gateway confiable, pero ese Gateway no está implementado en los archivos entregados. No debe presentarse como una cadena de autenticación completa.
