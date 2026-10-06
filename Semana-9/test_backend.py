// =====================================================
// AL SAHARA - SCRIPT PRINCIPAL
// Carrito + autenticación mediante API Gateway
// =====================================================

const GATEWAY_URL = ""; // mismo origen: el Gateway sirve el frontend

// =====================================================
// AUTENTICACIÓN
// =====================================================

async function authFetch(path, options = {}) {
    return fetch(`${GATEWAY_URL}${path}`, {
        ...options,
        credentials: "include",
        headers: {
            ...(options.headers || {}),
            "Content-Type": "application/json"
        }
    });
}

async function getCurrentUser() {
    try {
        const response = await authFetch("/auth/me");
        if (!response.ok) return null;
        return await response.json();
    } catch (error) {
        console.error("No se pudo consultar la sesión:", error);
        return null;
    }
}

async function cerrarSesion() {
    try {
        await authFetch("/auth/logout", { method: "POST" });
    } catch (error) {
        console.error("Error al cerrar sesión:", error);
    } finally {
        window.location.href = "login.html";
    }
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

async function actualizarAuthUI() {
    const area = document.querySelector("#auth-area");
    if (!area) return;

    const user = await getCurrentUser();

    if (!user) {
        area.innerHTML = '<a href="login.html" class="auth-link">Iniciar sesión</a>';
        return;
    }

    area.innerHTML = `
        <a href="cuenta.html" class="auth-link">Mi cuenta</a>
        <span class="auth-user">Hola, ${escapeHtml(user.username)}</span>
        <button type="button" class="auth-logout" id="logout-button">Cerrar sesión</button>
    `;

    document.querySelector("#logout-button")?.addEventListener("click", cerrarSesion);
}

async function iniciarSesion(username, password) {
    return authFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ username, password })
    });
}

async function cargarProductos() {
    try {
        const response = await authFetch("/api/products", { method: "GET" });

        if (response.status === 200) {
            const data = await response.json();
            const productos = Array.isArray(data.products) ? data.products : [];
            console.log("Productos cargados desde el Gateway:", productos);
            return productos;
        }

        if (response.status === 401) {
            console.warn("No hay una sesión activa. Error 401.");
        } else if (response.status === 403) {
            console.warn("La sesión no tiene permisos. Error 403.");
        }
    } catch (error) {
        console.error("Error al cargar productos:", error);
    }

    return [];
}

// =====================================================
// LOGIN
// =====================================================

document.addEventListener("DOMContentLoaded", () => {
    actualizarAuthUI();

    const loginForm = document.querySelector("#login-form");
    const loginMessage = document.querySelector("#login-message");

    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const username = document.querySelector("#username")?.value.trim();
            const password = document.querySelector("#login-password")?.value || "";

            if (!username || !password) return;

            if (loginMessage) {
                loginMessage.textContent = "Iniciando sesión...";
            }

            try {
                const response = await iniciarSesion(username, password);
                const data = await response.json().catch(() => ({}));

                if (!response.ok) {
                    if (loginMessage) {
                        loginMessage.textContent =
                            data.detail || "Usuario o contraseña incorrectos.";
                    }
                    return;
                }

                window.location.href = "index.html";
            } catch (error) {
                console.error("Error en el login:", error);
                if (loginMessage) {
                    loginMessage.textContent = "No se pudo conectar con el API Gateway.";
                }
            }
        });
    }

    // Si estamos en el menú, consultar el endpoint protegido.
    if (document.querySelector(".menu-page")) {
        cargarProductos();
    }
});


// =====================================================
// CARRITO AL SAHARA
// =====================================================

// =====================================================
// AGREGAR PRODUCTOS DESDE EL MENÚ
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll(".add-button");

    buttons.forEach(button => {

        button.addEventListener("click", () => {

            const product = button.dataset.product;
            const price = Number(button.dataset.price);

            let cart = JSON.parse(localStorage.getItem("alSaharaCart")) || [];

            const existingProduct = cart.find(
                item => item.product === product
            );

            if (existingProduct) {
                existingProduct.quantity++;
            } else {
                cart.push({
                    product: product,
                    price: price,
                    quantity: 1
                });
            }

            localStorage.setItem(
                "alSaharaCart",
                JSON.stringify(cart)
            );

            const originalText = button.innerHTML;
            button.innerHTML = "✓ Agregado";

            setTimeout(() => {
                button.innerHTML = originalText;
            }, 1200);
        });
    });
});


// =====================================================
// CARRITO
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

    const cartPage = document.querySelector(".cart-page");

    if (!cartPage) {
        return;
    }

    const cartProducts = document.querySelector(".cart-products");
    const itemCount = document.getElementById("cart-item-count");
    const subtotalElement = document.getElementById("cart-subtotal");
    const ivaElement = document.getElementById("cart-iva");
    const totalElement = document.getElementById("cart-total");

    const deliveryPrice = 2500;
    const ivaRate = 0.06;

    function formatPrice(number) {
        return "$" + number.toLocaleString("es-CL");
    }

    function getCart() {
        return JSON.parse(localStorage.getItem("alSaharaCart")) || [];
    }

    function saveCart(cart) {
        localStorage.setItem("alSaharaCart", JSON.stringify(cart));
    }

    function renderCart() {
        const cart = getCart();

        const oldProducts = cartProducts.querySelectorAll(
            ".cart-product, .empty-cart"
        );

        oldProducts.forEach(product => product.remove());

        if (cart.length === 0) {
            const emptyMessage = document.createElement("p");
            emptyMessage.classList.add("empty-cart");
            emptyMessage.textContent = "Tu carrito está vacío.";
            cartProducts.appendChild(emptyMessage);
            updateTotals();
            return;
        }

        cart.forEach(item => {
            const article = document.createElement("article");
            article.classList.add("cart-product");
            article.dataset.price = item.price;

            let image = "img/shawarma pollo.png";

            if (item.product === "Kebab de cordero picante") {
                image = "img/kebab cordero.png";
            } else if (item.product === "Plato de royal Hummus") {
                image = "img/hummus royal.png";
            } else if (item.product === "Falafel") {
                image = "img/falafel.png";
            } else if (item.product === "Shawarma de pollo") {
                image = "img/shawarma pollo.png";
            }

            article.innerHTML = `
                <img src="${image}" alt="${escapeHtml(item.product)}">

                <div class="cart-product-info">
                    <h2>${escapeHtml(item.product)}</h2>
                    <p>Producto del menú Al Sahara.</p>
                </div>

                <div class="quantity">
                    <button type="button" class="quantity-minus">−</button>
                    <span class="quantity-value">${item.quantity}</span>
                    <button type="button" class="quantity-plus">+</button>
                </div>

                <strong class="product-price">
                    ${formatPrice(item.price * item.quantity)}
                </strong>
            `;

            cartProducts.appendChild(article);
        });

        updateTotals();
    }

    function updateTotals() {
        const cart = getCart();

        let subtotal = 0;
        let totalItems = 0;

        cart.forEach(item => {
            subtotal += item.price * item.quantity;
            totalItems += item.quantity;
        });

        const iva = Math.round(subtotal * ivaRate);
        const total = subtotal + deliveryPrice + iva;

        if (itemCount) {
            itemCount.textContent = `(${totalItems} Items)`;
        }

        if (subtotalElement) {
            subtotalElement.textContent = formatPrice(subtotal);
        }

        if (ivaElement) {
            ivaElement.textContent = formatPrice(iva);
        }

        if (totalElement) {
            totalElement.textContent = formatPrice(total);
        }
    }

    document.addEventListener("click", event => {

        if (event.target.classList.contains("quantity-plus")) {
            const productElement = event.target.closest(".cart-product");
            if (!productElement) return;

            const products = getCart();
            const productName = productElement
                .querySelector(".cart-product-info h2")
                .textContent.trim();

            const product = products.find(
                item => item.product === productName
            );

            if (!product) return;

            product.quantity++;
            saveCart(products);
            renderCart();
        }

        if (event.target.classList.contains("quantity-minus")) {
            const productElement = event.target.closest(".cart-product");
            if (!productElement) return;

            const products = getCart();
            const productName = productElement
                .querySelector(".cart-product-info h2")
                .textContent.trim();

            const productIndex = products.findIndex(
                item => item.product === productName
            );

            if (productIndex === -1) return;

            products[productIndex].quantity--;

            if (products[productIndex].quantity <= 0) {
                products.splice(productIndex, 1);
            }

            saveCart(products);
            renderCart();
        }
    });

    renderCart();
});
