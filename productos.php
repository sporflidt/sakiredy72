<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Primera pagina</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>        
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>
    <body>
        <!-- Navbar -->
        <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
            <div class="container-fluid"> 
                <a class="navbar-brand" href="index.php"><img src="img/logo.png" width="80"></a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="collapsibleNavbar">
                    <ul class="navbar-nav">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="empresa.php" role="button" data-bs-toggle="dropdown">Empresa</a>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="#">Quienes Somos</a></li>
                                <li><a class="dropdown-item" href="#">Nuestro Equipo</a></li>
                                <li><a class="dropdown-item" href="#">Mision</a></li>
                            </ul>
                        </li>                        
                        <li class="nav-item">
                            <a class="nav-link" href="productos.php">Productos</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="servicios.php">Servicios</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="contacto.php">Contacto</a>
                        </li>  
                    </ul>
                </div>                
            </div>
        </nav>       
        <!-- Container -->
        <div class="container bg-morado" >
            <!-- Carousel -->
            <div id="demo" class="carousel slide" data-bs-ride="carousel">
                <!-- Indicators/dots -->
                <div class="carousel-indicators">
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="0" class="active"></button>
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="1"></button>
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="2"></button>
                </div>
                <!-- The slideshow/carousel -->
                <div class="carousel-inner">
                    <div class="carousel-item active">
                    <img src="img/ov.jpg" alt="Overworld" class="d-block w-100">
                    </div>
                    <div class="carousel-item">
                    <img src="img/nr.jpg" alt="Nether" class="d-block w-100">
                    </div>
                    <div class="carousel-item">
                    <img src="img/thnd.jpg" alt="The End" class="d-block w-100">
                    </div>
                </div>
                <!-- Left and right controls/icons -->
                <button class="carousel-control-prev" type="button" data-bs-target="#demo" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon"></span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#demo" data-bs-slide="next">
                    <span class="carousel-control-next-icon"></span>
                </button>
            </div>
            <div class="container-fluid">
                <div class="row mb-5">
                    <div class="col-12 col-md-4">
                        <div class="card h-100">
                            <img class="card-img-top" src="img/beacon.png" alt="Card image">
                            <div class="card-body d-flex flex-column">
                                <h4 class="card-title">Faro de luz</h4>
                                <p class="card-text">Compra nuestro faro de luz 3000.</p>
                                <a href="#" class="btn btn-primary mt-auto">Comprar</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-md-4">
                        <div class="card h-100">
                            <img class="card-img-top" src="img/bedrock.png" alt="Card image">
                            <div class="card-body d-flex flex-column">
                                <h4 class="card-title">Bedrock</h4>
                                <p class="card-text">Compra nuestra piedra base.</p>
                                <a href="#" class="btn btn-primary mt-auto">Comprar</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-md-4">
                        <div class="card h-100">
                            <img class="card-img-top" src="img/diamante.png" alt="Card image">
                            <div class="card-body d-flex flex-column">
                                <h4 class="card-title">Diamante</h4>
                                <p class="card-text">Compra nuestro cubo de diamante de calidad.</p>
                                <a href="#" class="btn btn-primary mt-auto">Comprar</a>
                            </div>
                        </div>
                    </div>                                                                                                                                                                           
                </div>
            </div>
        </div>
        <!-- Footer -->   
        <div class="container-fluid bg-dark text-center py-2">
    <div style="color:white">
        <strong>sakiredy72</strong>
    </div>
</div>
        <!-- Modal -->     
    </body>
</html>