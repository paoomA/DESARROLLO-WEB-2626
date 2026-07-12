const formulario = document.getElementById("formProducto");
const mensaje = document.getElementById("mensaje");
const listaProductos = document.getElementById("listaProductos");
const contadorProductos = document.getElementById("contadorProductos");
const catalogoProductos = document.getElementById("catalogoProductos");
let totalProductos = 0;

const campoNombre = document.getElementById("nombre");
const campoDescripcion = document.getElementById("descripcion");
const campoCategoria = document.getElementById("categoria");
const campoPrecio = document.getElementById("precio");
const campoCantidad = document.getElementById("cantidad");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

const productos = [];
function renderizarProductos() {

    catalogoProductos.innerHTML = "";

    if (productos.length === 0) {

    catalogoProductos.innerHTML = `
        <div class="col-12 text-center">
            <div class="alert alert-warning">
                No hay productos disponibles en este momento.
            </div>
        </div>
    `;

    return;
}

    productos.forEach(function(producto){

        catalogoProductos.innerHTML += `

        <div class="col-md-4 mb-4">

            <div class="card producto-card h-100">

                <img src="${producto.imagen}" class="card-img-top" alt="${producto.nombre}">

                <div class="card-body">

                    <h5 class="card-title">${producto.nombre}</h5>

                    <p class="card-text">
                        ${producto.descripcion}
                    </p>

                    <p>
                        <strong>Categoría:</strong> ${producto.categoria}
                    </p>

                    <p class="precio">
                        ${producto.precio}
                    </p>
                    <p>
                    <strong>Cantidad disponible:</strong> ${producto.cantidad}
                    </p>

                </div>

            </div>

        </div>

        `;

    });

}
function validarNombre(){

    const nombre = campoNombre.value.trim();

    if(nombre === ""){

        errorNombre.textContent = "El nombre de la prenda es obligatorio.";

        campoNombre.classList.add("is-invalid");
        campoNombre.classList.remove("is-valid");

        return false;

    }

    if(nombre.length < 3){

        errorNombre.textContent = "Debe ingresar al menos 3 caracteres.";

        campoNombre.classList.add("is-invalid");
        campoNombre.classList.remove("is-valid");

        return false;

    }

    errorNombre.textContent = "";

    campoNombre.classList.remove("is-invalid");
    campoNombre.classList.add("is-valid");

    return true;

}

function validarDescripcion(){

    const descripcion = campoDescripcion.value.trim();

    if(descripcion === ""){

        errorDescripcion.textContent = "La descripción es obligatoria.";

        campoDescripcion.classList.add("is-invalid");
        campoDescripcion.classList.remove("is-valid");

        return false;

    }

    if(descripcion.length < 10){

        errorDescripcion.textContent = "La descripción debe tener al menos 10 caracteres.";

        campoDescripcion.classList.add("is-invalid");
        campoDescripcion.classList.remove("is-valid");

        return false;

    }

    errorDescripcion.textContent = "";

    campoDescripcion.classList.remove("is-invalid");
    campoDescripcion.classList.add("is-valid");

    return true;

}

function validarCategoria(){

    if(campoCategoria.value === ""){

        errorCategoria.textContent = "Seleccione una categoría.";

        campoCategoria.classList.add("is-invalid");
        campoCategoria.classList.remove("is-valid");

        return false;

    }

    errorCategoria.textContent = "";

    campoCategoria.classList.remove("is-invalid");
    campoCategoria.classList.add("is-valid");

    return true;

}
campoNombre.addEventListener("input", validarNombre);
campoNombre.addEventListener("blur", validarNombre);

campoDescripcion.addEventListener("input", validarDescripcion);
campoDescripcion.addEventListener("blur", validarDescripcion);

campoCategoria.addEventListener("change", validarCategoria);
campoCategoria.addEventListener("blur", validarCategoria);

formulario.addEventListener("submit", function(event){

    event.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value;
    const precio = campoPrecio.value.trim();
    const cantidad = campoCantidad.value.trim();

let imagenProducto = "";

switch(categoria){

    case "Vestidos":
        imagenProducto = "resources/img/vestido.jpeg";
        break;

    case "Blusas":
        imagenProducto = "resources/img/blusas.jpeg";
        break;

    case "Jeans":
        imagenProducto = "resources/img/jeans.jpeg";
        break;

    case "Faldas":
        imagenProducto = "resources/img/faldas.jpg";
        break;

    case "Bodys":
        imagenProducto = "resources/img/body.jpg";
        break;

    case "Conjuntos":
        imagenProducto = "resources/img/conjuntos.jpg";
        break;

    case "Chaquetas de mezclilla":
        imagenProducto = "resources/img/chaquetas.jpg";
        break;

    case "Blazers":
        imagenProducto = "resources/img/blazers.jpeg";
        break;

    case "Shorts":
        imagenProducto = "resources/img/shorts.jpeg";
        break;

    case "Enterizos":
        imagenProducto = "resources/img/enterizos.jpg";
        break;

    case "Conjuntos Deportivos":
        imagenProducto = "resources/img/conj_deportivos.png";
        break;

    case "Crop Tops":
        imagenProducto = "resources/img/crop_tops.png";
        break;

    default:
        imagenProducto = "resources/img/moda1.jpeg";
}
    if(!validarNombre() || !validarDescripcion() || !validarCategoria()){

    mensaje.innerHTML = `
        <div class="alert alert-danger">
            Corrija los campos antes de registrar el producto.
        </div>
    `;

    return;
}

    mensaje.innerHTML = `
    <div class="alert alert-success">
        Producto registrado correctamente.
    </div>
    `;
productos.push({

    nombre: nombre,
    categoria: categoria,
    precio: "$" + precio,
    cantidad: cantidad,
    descripcion: descripcion,
    imagen: imagenProducto

});

renderizarProductos();
    const tarjeta = document.createElement("div");

    tarjeta.className = "card p-3 mt-3 shadow";

    tarjeta.innerHTML = `
        <h5>${nombre}</h5>
        <p><strong>Descripción:</strong> ${descripcion}</p>
        <p><strong>Categoría:</strong> ${categoria}</p>
    `;
const botonEliminar = document.createElement("button");

botonEliminar.textContent = "Eliminar";

botonEliminar.className = "btn btn-danger mt-2";

botonEliminar.addEventListener("click", function(){

    const indice = productos.findIndex(function(producto){

        return producto.nombre === nombre &&
               producto.categoria === categoria;

    });

    if(indice !== -1){

        productos.splice(indice, 1);

    }

    renderizarProductos();

    tarjeta.remove();

   contadorProductos.textContent = productos.length;

});

    tarjeta.appendChild(botonEliminar);

    listaProductos.appendChild(tarjeta);

   contadorProductos.textContent = productos.length;

    formulario.reset();

campoNombre.classList.remove("is-valid");
campoDescripcion.classList.remove("is-valid");
campoCategoria.classList.remove("is-valid");

errorNombre.textContent = "";
errorDescripcion.textContent = "";
errorCategoria.textContent = "";

});

const formContacto = document.getElementById("formContacto");
const mensajeFormulario = document.getElementById("respuestaContacto");

const campoNombreContacto = document.getElementById("nombreContacto");
const campoCorreo = document.getElementById("correoContacto");
const campoTipo = document.getElementById("tipoConsulta");
const campoMensaje = document.getElementById("mensajeContacto");

const errorNombreContacto = document.getElementById("errorNombreContacto");
const errorCorreo = document.getElementById("errorCorreo");
const errorTipo = document.getElementById("errorTipo");
const errorMensajeContacto = document.getElementById("errorMensajeContacto");

function validarNombreContacto(){

    const nombre = campoNombreContacto.value.trim();

    if(nombre === ""){

        errorNombreContacto.textContent = "El nombre es obligatorio.";

        campoNombreContacto.classList.add("is-invalid");
        campoNombreContacto.classList.remove("is-valid");

        return false;

    }

    if(nombre.length < 3){

        errorNombreContacto.textContent = "Debe ingresar al menos 3 caracteres.";

        campoNombreContacto.classList.add("is-invalid");
        campoNombreContacto.classList.remove("is-valid");

        return false;

    }

    errorNombreContacto.textContent = "";

    campoNombreContacto.classList.remove("is-invalid");
    campoNombreContacto.classList.add("is-valid");

    return true;

}

function validarCorreo(){

    const correo = campoCorreo.value.trim();

    if(correo === ""){

        errorCorreo.textContent = "El correo es obligatorio.";

        campoCorreo.classList.add("is-invalid");
        campoCorreo.classList.remove("is-valid");

        return false;

    }

    const expresionCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if(!expresionCorreo.test(correo)){

        errorCorreo.textContent = "Ingrese un correo válido.";

        campoCorreo.classList.add("is-invalid");
        campoCorreo.classList.remove("is-valid");

        return false;

    }

    errorCorreo.textContent = "";

    campoCorreo.classList.remove("is-invalid");
    campoCorreo.classList.add("is-valid");

    return true;

}

function validarTipo(){

    if(campoTipo.value === ""){

        errorTipo.textContent = "Seleccione un tipo de consulta.";

        campoTipo.classList.add("is-invalid");
        campoTipo.classList.remove("is-valid");

        return false;

    }

    errorTipo.textContent = "";

    campoTipo.classList.remove("is-invalid");
    campoTipo.classList.add("is-valid");

    return true;

}

function validarMensajeContacto(){

    const mensaje = campoMensaje.value.trim();

    if(mensaje === ""){

        errorMensajeContacto.textContent = "El mensaje es obligatorio.";

        campoMensaje.classList.add("is-invalid");
        campoMensaje.classList.remove("is-valid");

        return false;

    }

    if(mensaje.length < 10){

        errorMensajeContacto.textContent = "El mensaje debe tener al menos 10 caracteres.";

        campoMensaje.classList.add("is-invalid");
        campoMensaje.classList.remove("is-valid");

        return false;

    }

    errorMensajeContacto.textContent = "";

    campoMensaje.classList.remove("is-invalid");
    campoMensaje.classList.add("is-valid");

    return true;

}
campoNombreContacto.addEventListener("input", validarNombreContacto);
campoNombreContacto.addEventListener("blur", validarNombreContacto);

campoCorreo.addEventListener("input", validarCorreo);
campoCorreo.addEventListener("blur", validarCorreo);

campoTipo.addEventListener("change", validarTipo);
campoTipo.addEventListener("blur", validarTipo);

campoMensaje.addEventListener("input", validarMensajeContacto);
campoMensaje.addEventListener("blur", validarMensajeContacto);

formContacto.addEventListener("submit", function(event){

    event.preventDefault();

    const nombre = document.getElementById("nombreContacto").value.trim();
    const correo = document.getElementById("correoContacto").value.trim();
    const tipo = document.getElementById("tipoConsulta").value;
    const mensaje = document.getElementById("mensajeContacto").value.trim();

    if(
    !validarNombreContacto() ||
    !validarCorreo() ||
    !validarTipo() ||
    !validarMensajeContacto()
){

    mensajeFormulario.innerHTML = `
    <div class="alert alert-danger mt-3">
        Corrija los campos antes de enviar el mensaje.
    </div>
    `;

    return;
}

    mensajeFormulario.innerHTML = `
    <div class="alert alert-success mt-3">
        Mensaje preparado correctamente. Será enviado por WhatsApp.
    </div>
    `;

    const texto = `Hola, soy ${nombre}.
Correo: ${correo}
Tipo de consulta: ${tipo}
Mensaje: ${mensaje}`;

    const url = `https://wa.me/593968359008?text=${encodeURIComponent(texto)}`;

   window.open(url, "_blank");

formContacto.reset();

campoNombreContacto.classList.remove("is-valid");
campoCorreo.classList.remove("is-valid");
campoTipo.classList.remove("is-valid");
campoMensaje.classList.remove("is-valid");

errorNombreContacto.textContent = "";
errorCorreo.textContent = "";
errorTipo.textContent = "";
errorMensajeContacto.textContent = "";

setTimeout(function(){

    document.getElementById("respuestaContacto").innerHTML = "";

}, 3000);

}); 
renderizarProductos();