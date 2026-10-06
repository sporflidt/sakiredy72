/* =====================================================
   PÁGINA DE REGISTRO
===================================================== */

.register-page {

    min-height: 540px;

    padding: 40px 5% 55px;

    display: grid;

    grid-template-columns: 1fr 1fr;

    align-items: center;

    gap: 70px;

    background: var(--cream);

}


/* =====================================================
   INTRODUCCIÓN
===================================================== */

.register-intro {

    max-width: 600px;

}


.register-eyebrow {

    display: block;

    margin-bottom: 10px;

    color: var(--gold);

    font-size: 10px;

    font-weight: bold;

    letter-spacing: 1.5px;

}


.register-intro h1 {

    max-width: 560px;

    margin-bottom: 12px;

    color: var(--burgundy);

    font-family: Georgia, "Times New Roman", serif;

    font-size: clamp(34px, 4vw, 50px);

    line-height: 1.02;

}


.register-description {

    max-width: 520px;

    margin-bottom: 20px;

    color: #756b68;

    font-size: 16px;

    line-height: 1.55;

}


/* =====================================================
   BENEFICIOS
===================================================== */

.register-benefit {

    display: flex;

    align-items: flex-start;

    gap: 10px;

    margin-bottom: 12px;

}


.benefit-icon {

    width: 26px;
    height: 26px;

    flex-shrink: 0;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background: white;

    color: var(--gold);

    font-size: 14px;

}


.register-benefit h3 {

    margin-bottom: 2px;

    color: var(--burgundy);

    font-family: Georgia, "Times New Roman", serif;

    font-size: 14px;

}


.register-benefit p {

    color: #817876;

    font-size: 10px;

    line-height: 1.4;

}


/* =====================================================
   IMAGEN
===================================================== */

.register-image {

    width: 100%;

    max-width: 500px;

    margin-top: 20px;

    overflow: hidden;

    border-radius: 9px;

}


.register-image img {

    width: 100%;

    height: 130px;

    display: block;

    object-fit: cover;

}


/* =====================================================
   FORMULARIO
===================================================== */

.register-form-container {

    width: 100%;

    display: flex;

    justify-content: center;

}


.register-form {

    width: 100%;

    max-width: 390px;

    padding: 28px;

    background: white;

    border-radius: 14px;

}


.register-form h2 {

    margin-bottom: 4px;

    color: var(--burgundy);

    font-family: Georgia, "Times New Roman", serif;

    font-size: 28px;

}


.form-subtitle {

    margin-bottom: 19px;

    color: #817876;

    font-size: 14px;

}


/* =====================================================
   CAMPOS
===================================================== */

.form-group {

    margin-bottom: 11px;

}


.form-group label {

    display: block;

    margin-bottom: 5px;

    color: #3e3030;

    font-size: 14px;

    font-weight: bold;

}


.form-group input {

    width: 100%;

    height: 27px;

    padding: 0 10px;

    border: 1px solid #eee8e1;

    border-radius: 6px;

    outline: none;

    background: #faf7f3;

    color: #4d4542;

    font-size: 14px;

    box-sizing: border-box;

}


.form-group input:focus {

    border-color: #d8a06a;

}


/* =====================================================
   BOTÓN REGISTRO
===================================================== */

.register-button {

    width: 100%;

    height: 31px;

    margin-top: 3px;

    border: none;

    border-radius: 20px;

    background: var(--burgundy);

    color: white;

    font-size: 14px;

    font-weight: bold;

    cursor: pointer;

}


.register-button:hover {

    background: #741a28;

}


/* =====================================================
   REGISTRO CON REDES
===================================================== */

.social-register {

    margin-top: 12px;

    text-align: center;

}


.social-register > span {

    display: block;

    margin-bottom: 8px;

    color: #817876;

    font-size: 14px;

}


.social-register-buttons {

    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 7px;

}


.social-register-buttons button {

    height: 24px;

    border: 1px solid #eee8e1;

    border-radius: 5px;

    background: white;

    color: #594d4a;

    font-size: 14px;

    cursor: pointer;

}


.social-register-buttons button strong {

    margin-right: 4px;

    color: var(--burgundy);

}


/* =====================================================
   LOGIN
===================================================== */

.already-account {

    margin-top: 15px;

    text-align: center;

    color: #817876;

    font-size: 14px;

}


.already-account a {

    color: var(--gold);

    font-weight: bold;

}


/* =====================================================
   RESPONSIVE
===================================================== */

@media (max-width: 800px) {

    .register-page {

        grid-template-columns: 1fr;

        padding: 45px 6%;

        gap: 45px;

    }


    .register-intro {

        max-width: 600px;

        margin: auto;

    }


    .register-image {

        max-width: 600px;

    }


    .register-form-container {

        max-width: 500px;

        margin: auto;

    }

}


@media (max-width: 500px) {

    .register-page {

        padding: 35px 20px;

    }


    .register-intro h1 {

        font-size: 36px;

    }


    .register-form {

        padding: 22px;

    }

}