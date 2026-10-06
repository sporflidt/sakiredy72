/* =====================================================
   CATEGORÍAS DEL MENÚ
===================================================== */

.menu-categories {

    padding: 0 45px 16px;

    display: grid;

    grid-template-columns: repeat(6, 1fr);

    gap: 22px;

    background: var(--cream);

}

.menu-category {
    min-height: 150px;

    padding: 12px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    background: white;
    border-radius: 9px;

    transition: transform 0.2s ease;
}

.menu-category:hover {

    transform: translateY(-3px);

}

.menu-category img {
    width: 82px;
    height: 82px;

    margin-bottom: 7px;

    object-fit: cover;
    border-radius: 50%;
}

.menu-category h3 {

    color: var(--burgundy);

    font-family: Georgia, "Times New Roman", serif;

    font-size: 24px;
}

.menu-category span {

    margin-top: 3px;

    color: #817876;

    font-size: 14px;

}


/* =====================================================
   SECCIONES DE PRODUCTOS
===================================================== */

.menu-section {

    padding: 15px 45px 37px;

    background: white;

}

.menu-section + .menu-section {

    padding-top: 0;

}

.menu-section h2 {

    margin-bottom: 11px;

    color: var(--burgundy);

    font-family: Georgia, "Times New Roman", serif;

    font-size: 20px;

}


/* =====================================================
   GRID DE PRODUCTOS
===================================================== */

.menu-products {

    display: grid;

    grid-template-columns: repeat(4, 1fr);

    gap: 19px;

}


/* =====================================================
   PRODUCTO
===================================================== */

.menu-product {

    display: flex;

    flex-direction: column;

    min-width: 0;

}

.menu-product > img {

    width: 100%;

    height: 125px;

    display: block;

    object-fit: cover;

    border-radius: 12px 12px 0 0;

}


/* INFORMACIÓN */

.menu-product-info {

    min-height: 128px;

    padding: 12px 13px 8px;

}

.menu-product-info h3 {

    margin-bottom: 5px;

    color: var(--burgundy);

    font-family: Georgia, "Times New Roman", serif;

    font-size: 16px;

    line-height: 1.15;

}

.menu-product-info p {

    color: #746b68;

    font-size: 12px;

    line-height: 1.45;

}


/* =====================================================
   PRECIO + BOTÓN
===================================================== */

.menu-product-bottom {

    min-height: 40px;

    padding: 10px 13px;

    border-top: 1px solid var(--border);

    display: flex;

    align-items: center;

    justify-content: space-between;

}

.menu-product-bottom strong {

    color: var(--gold);

    font-family: Georgia, "Times New Roman", serif;

    font-size: 20px;

}

.menu-product-bottom .add-button {

    padding: 8px 14px;

    font-size: 16px;

}


/* =====================================================
   SECCIONES VACÍAS
===================================================== */

.empty-category {

    display: none;

}