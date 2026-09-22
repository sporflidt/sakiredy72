
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

            // Obtener carrito guardado
            let cart = JSON.parse(localStorage.getItem("alSaharaCart")) || [];

            // Buscar si el producto ya existe
            const existingProduct = cart.find(
                item => item.product === product
            );

            if (existingProduct) {

                // Si ya existe, aumentar cantidad
                existingProduct.quantity++;

            } else {

                // Si no existe, agregarlo
                cart.push({
                    product: product,
                    price: price,
                    quantity: 1
                });

            }

            // Guardar carrito
            localStorage.setItem(
                "alSaharaCart",
                JSON.stringify(cart)
            );


            // Feedback visual
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

    // Si no estamos en carrito.php, salir
    if (!cartPage) {
        return;
    }


    // =================================================
    // ELEMENTOS
    // =================================================

    const cartProducts =
        document.querySelector(".cart-products");

    const itemCount =
        document.getElementById("cart-item-count");

    const subtotalElement =
        document.getElementById("cart-subtotal");

    const ivaElement =
        document.getElementById("cart-iva");

    const totalElement =
        document.getElementById("cart-total");


    const deliveryPrice = 2500;
    const ivaRate = 0.06;


    // =================================================
    // FORMATO DE PRECIO
    // =================================================

    function formatPrice(number) {

        return "$" + number.toLocaleString("es-CL");

    }


    // =================================================
    // OBTENER CARRITO
    // =================================================

    function getCart() {

        return JSON.parse(
            localStorage.getItem("alSaharaCart")
        ) || [];

    }


    // =================================================
    // GUARDAR CARRITO
    // =================================================

    function saveCart(cart) {

        localStorage.setItem(
            "alSaharaCart",
            JSON.stringify(cart)
        );

    }


    // =================================================
    // MOSTRAR PRODUCTOS
    // =================================================

    function renderCart() {

        const cart = getCart();


        // Eliminar productos escritos originalmente
        // en carrito.php
        const oldProducts =
            cartProducts.querySelectorAll(".cart-product, .empty-cart");

        oldProducts.forEach(product => {
            product.remove();
        });


        // Si el carrito está vacío
        if (cart.length === 0) {

            const emptyMessage =
                document.createElement("p");

            emptyMessage.classList.add("empty-cart");

            emptyMessage.textContent =
                "Tu carrito está vacío.";

            cartProducts.appendChild(emptyMessage);

            updateTotals();

            return;
        }


        // Crear productos guardados
        cart.forEach((item, index) => {

            const article =
                document.createElement("article");

            article.classList.add("cart-product");

            article.dataset.price = item.price;


            // Imagen según el producto
            let image = "img/shawarma pollo.png";


            if (
                item.product ===
                "Kebab de cordero picante"
            ) {

                image = "img/kebab cordero.png";

            }

            else if (
                item.product ===
                "Plato de royal Hummus"
            ) {

                image = "img/hummus royal.png";

            }

            else if (
                item.product ===
                "Falafel"
            ) {

                image = "img/falafel.png";

            }

            else if (
                item.product ===
                "Shawarma de pollo"
            ) {

                image = "img/shawarma pollo.png";

            }


            article.innerHTML = `

                <img
                    src="${image}"
                    alt="${item.product}"
                >

                <div class="cart-product-info">

                    <h2>
                        ${item.product}
                    </h2>

                    <p>
                        Producto del menú Al Sahara.
                    </p>

                </div>


                <div class="quantity">

                    <button
                        type="button"
                        class="quantity-minus"
                    >
                        −
                    </button>


                    <span class="quantity-value">
                        ${item.quantity}
                    </span>


                    <button
                        type="button"
                        class="quantity-plus"
                    >
                        +
                    </button>

                </div>


                <strong class="product-price">
                    ${formatPrice(
                        item.price * item.quantity
                    )}
                </strong>

            `;


            cartProducts.appendChild(article);

        });


        updateTotals();

    }


    // =================================================
    // ACTUALIZAR TOTALES
    // =================================================

    function updateTotals() {

        const cart = getCart();

        let subtotal = 0;
        let totalItems = 0;


        cart.forEach(item => {

            subtotal +=
                item.price * item.quantity;

            totalItems +=
                item.quantity;

        });


        const iva =
            Math.round(subtotal * ivaRate);


        const total =
            subtotal +
            deliveryPrice +
            iva;


        // Items
        if (itemCount) {

            itemCount.textContent =
                `(${totalItems} Items)`;

        }


        // Subtotal
        if (subtotalElement) {

            subtotalElement.textContent =
                formatPrice(subtotal);

        }


        // IVA
        if (ivaElement) {

            ivaElement.textContent =
                formatPrice(iva);

        }


        // Total
        if (totalElement) {

            totalElement.textContent =
                formatPrice(total);

        }

    }


    // =================================================
    // BOTONES + Y -
    // =================================================

    document.addEventListener("click", event => {


        // =================================================
        // +
        // =================================================

        if (
            event.target.classList.contains(
                "quantity-plus"
            )
        ) {

            const productElement =
                event.target.closest(".cart-product");

            if (!productElement) {
                return;
            }


            const products =
                getCart();


            const productName =
                productElement.querySelector(
                    ".cart-product-info h2"
                ).textContent.trim();


            const product =
                products.find(
                    item => item.product === productName
                );


            if (!product) {
                return;
            }


            product.quantity++;


            saveCart(products);

            renderCart();

        }


        // =================================================
        // -
        // =================================================

        if (
            event.target.classList.contains(
                "quantity-minus"
            )
        ) {

            const productElement =
                event.target.closest(".cart-product");

            if (!productElement) {
                return;
            }


            const products =
                getCart();


            const productName =
                productElement.querySelector(
                    ".cart-product-info h2"
                ).textContent.trim();


            const productIndex =
                products.findIndex(
                    item => item.product === productName
                );


            if (productIndex === -1) {
                return;
            }


            products[productIndex].quantity--;


            // Si llega a 0, eliminar
            if (
                products[productIndex].quantity <= 0
            ) {

                products.splice(productIndex, 1);

            }


            saveCart(products);

            renderCart();

        }

    });


    // =================================================
    // CARGAR CARRITO AL ENTRAR
    // =================================================

    renderCart();

});