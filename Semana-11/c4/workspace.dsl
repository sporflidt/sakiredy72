workspace "Al Sahara" "Modelo C4 basado en los archivos disponibles del proyecto Al Sahara." {

    model {
        visitante = person "Visitante" "Navega las páginas públicas del sitio web."
        apiClient = person "Consumidor HTTP" "Cliente externo o herramienta de pruebas que consume directamente las API. No representa una integración existente desde el frontend."

        vault = softwareSystem "HashiCorp Vault" "Gestor externo de secretos. Los servicios leen secretos desde el motor KV v2." {
            tags "External"
        }

        alSahara = softwareSystem "Plataforma Al Sahara" "Sitio web de restaurante y servicios backend disponibles en la versión revisada." {

            frontend = container "Frontend Web" "Páginas estáticas de inicio, menú, registro y carrito. El menú y los precios están definidos en HTML." "HTML, CSS y JavaScript" {
                paginas = component "Páginas HTML" "Presentan inicio, menú, registro y carrito. El formulario de registro es visual y no envía datos al backend." "HTML"
                catalogo = component "Catálogo estático" "Define productos, descripciones y precios directamente en las páginas HTML." "HTML"
                gestorCarrito = component "Gestor del carrito" "Agrega productos, cambia cantidades y calcula subtotal, IVA y total." "JavaScript"
                almacenamientoLocal = component "Almacenamiento del carrito" "Lee y escribe el carrito bajo la clave alSaharaCart." "Web Storage API (localStorage)"
            }

            authService = container "Auth Service" "Gestiona el inicio de sesión, introspección y revocación de sesiones. Usuarios y sesiones se mantienen en memoria." "Python 3.11, FastAPI (puerto 8100 en Compose)" {
                authApi = component "API de autenticación" "Expone GET /health y POST /login, /introspect y /logout." "FastAPI"
                usersRepository = component "Repositorio de usuarios" "Contiene las cuentas de prueba y sus hashes Argon2id en el diccionario USERS." "Memoria"
                credentialVerifier = component "Verificador de credenciales" "Verifica la contraseña recibida contra password_hash mediante Argon2id." "argon2-cffi"
                sessionManager = component "Gestor de sesiones" "Genera tokens aleatorios, registra sesiones y aplica una expiración de 900 segundos." "Memoria y secrets"
                authSecretValidator = component "Validador de secreto interno" "Protege /introspect y /logout mediante X-Gateway-Secret y secrets.compare_digest." "Python secrets"
                authVaultClient = component "Cargador de secreto Auth" "Obtiene auth_introspection_secret mediante common_secrets.vault_secret al cargar el módulo." "hvac, Vault KV v2"
            }

            backendApi = container "Backend API" "Expone operaciones de consulta de productos y pedidos y eliminación administrativa de productos. Los datos se mantienen en memoria." "Python 3.11, FastAPI (puerto 9000 en Compose)" {
                backendRoutes = component "API REST" "Expone GET /health, GET /products, GET /orders y DELETE /products/{product_id}." "FastAPI"
                backendSecretValidator = component "Validador de secreto Gateway" "Protege productos y pedidos mediante X-Gateway-Secret y secrets.compare_digest." "Python secrets"
                adminPolicy = component "Política de administrador" "Exige que X-Authenticated-Roles incluya el texto admin para eliminar productos." "FastAPI Dependency"
                productsRepository = component "Repositorio de productos" "Mantiene la lista PRODUCTS en memoria; permite consultar y eliminar productos." "Memoria"
                ordersRepository = component "Repositorio de pedidos" "Mantiene la lista ORDERS en memoria; actualmente solo permite consultarla." "Memoria"
                backendVaultClient = component "Cargador de secreto Backend" "Obtiene backend_shared_secret mediante common_secrets.vault_secret al cargar el módulo." "hvac, Vault KV v2"
            }
        }

        visitante -> alSahara "Navega el sitio web"
        apiClient -> alSahara "Consume directamente las API disponibles"

        visitante -> frontend "Abre las páginas estáticas"
        apiClient -> authService "Consume la API de autenticación directamente"
        authService -> apiClient "Devuelve respuestas HTTP al consumidor"
        apiClient -> backendApi "Consume la API protegida directamente"
        backendApi -> apiClient "Devuelve respuestas HTTP al consumidor"

        alSahara -> vault "Obtiene secretos técnicos desde KV v2"
        authService -> vault "Lee auth_introspection_secret al iniciar"
        backendApi -> vault "Lee backend_shared_secret al iniciar"

        paginas -> catalogo "Presenta el catálogo definido en HTML"
        catalogo -> gestorCarrito "Permite agregar productos"
        paginas -> gestorCarrito "Muestra la página y controles del carrito"
        gestorCarrito -> almacenamientoLocal "Lee y guarda alSaharaCart"

        authApi -> usersRepository "Busca las cuentas registradas en memoria"
        authApi -> credentialVerifier "Verifica la contraseña durante POST /login"
        authApi -> sessionManager "Crea, consulta y revoca sesiones"
        authApi -> authSecretValidator "Valida el secreto en /introspect y /logout"
        authVaultClient -> vault "Lee auth_introspection_secret desde secret/gateway"

        backendRoutes -> backendSecretValidator "Valida X-Gateway-Secret en productos y pedidos"
        backendRoutes -> adminPolicy "Aplica la política adicional en DELETE de productos"
        backendRoutes -> productsRepository "Consulta o elimina productos"
        backendRoutes -> ordersRepository "Consulta pedidos"
        backendVaultClient -> vault "Lee backend_shared_secret desde secret/gateway"
    }

    views {
        systemContext alSahara "C1_Contexto" {
            include *
            autoLayout lr
        }

        container alSahara "C2_Contenedores" {
            include *
            autoLayout lr
        }

        component frontend "C3_Frontend" {
            include *
            autoLayout lr
        }

        component authService "C3_Auth" {
            include *
            autoLayout lr
        }

        component backendApi "C3_Backend" {
            include *
            autoLayout lr
        }

        dynamic authService "Dyn_Login" {
            apiClient -> authService "POST /login con username y password"
            authApi -> usersRepository "Busca el usuario"
            authApi -> credentialVerifier "Verifica password_hash con Argon2id"
            authApi -> sessionManager "Genera token aleatorio y registra expires_at"
            authService -> apiClient "200: access_token, token_type y expires_in"
            autoLayout lr
        }

        dynamic authService "Dyn_Introspeccion" {
            apiClient -> authService "POST /introspect con X-Gateway-Secret"
            authApi -> authSecretValidator "Valida el secreto interno"
            authApi -> sessionManager "Busca token y comprueba expiración"
            authService -> apiClient "Devuelve active y, si corresponde, identidad y roles"
            autoLayout lr
        }

        dynamic backendApi "Dyn_ConsultaProductos" {
            apiClient -> backendApi "GET /products con X-Gateway-Secret"
            backendRoutes -> backendSecretValidator "Verifica el secreto compartido"
            backendRoutes -> productsRepository "Lee PRODUCTS"
            backendApi -> apiClient "200: lista de productos y authenticated_client"
            autoLayout lr
        }

        dynamic backendApi "Dyn_EliminarProducto" {
            apiClient -> backendApi "DELETE /products/{product_id} con secreto y rol admin"
            backendRoutes -> backendSecretValidator "Verifica X-Gateway-Secret"
            backendRoutes -> adminPolicy "Comprueba X-Authenticated-Roles"
            backendRoutes -> productsRepository "Busca y elimina el producto"
            backendApi -> apiClient "Devuelve producto eliminado o error 404"
            autoLayout lr
        }

        dynamic alSahara "Dyn_SecretBootstrap" {
            authVaultClient -> vault "Lee auth_introspection_secret al importar Auth Service"
            backendVaultClient -> vault "Lee backend_shared_secret al importar Backend API"
            autoLayout lr
        }

        styles {
            element "Person" {
                shape person
                background #475569
                color #ffffff
            }

            element "Software System" {
                background #92400e
                color #ffffff
            }

            element "External" {
                background #475569
                color #ffffff
            }

            element "Container" {
                background #d97706
                color #ffffff
            }

            element "Component" {
                background #fbbf24
                color #1f2937
            }
        }
    }
}
