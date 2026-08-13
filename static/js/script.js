const formulario = document.getElementById("formProducto");
const mensaje = document.getElementById("mensaje");
const spinnerCarga = document.getElementById("spinnerCarga");
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
const errorPrecio = document.getElementById("errorPrecio");
const errorCantidad = document.getElementById("errorCantidad");

const productos = [];
function renderizarProductos() {

    catalogoProductos.innerHTML = "";

    if (productos.length === 0) {

catalogoProductos.innerHTML = `
<div class="col-12">

<div class="alert alert-warning d-flex justify-content-center align-items-center text-center" role="alert">

<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
<use xlink:href="#exclamation-triangle-fill"></use>
</svg>

<div>
No hay productos disponibles en este momento.
</div>

</div>

</div>
`;

    return;
}

    productos.forEach(function(producto, index){

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
    <strong>Cantidad disponible:</strong>
    ${producto.cantidad}
</p>

<div class="d-grid gap-2 mt-3">

    <button
        class="btn btn-outline-primary"
        onclick="verProducto(${index})">
        Ver información
    </button>

    <button
    class="btn btn-outline-danger"
    onclick="abrirModalEliminar(${index})">

    Eliminar

</button>

</div>

                </div>

            </div>

        </div>

        `;

    });

}
function validarNombre(){

    const nombre = campoNombre.value.trim();
    const soloLetras = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;

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
    if(!soloLetras.test(nombre)){

    errorNombre.textContent = "Solo se permiten letras.";

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
    if(!/[A-Za-zÁÉÍÓÚáéíóúÑñ]/.test(descripcion)){

    errorDescripcion.textContent = "La descripción debe contener texto.";

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
function validarPrecio(){

    const precio = campoPrecio.value.trim();

    if(precio === ""){

        errorPrecio.textContent = "El precio es obligatorio.";

        campoPrecio.classList.add("is-invalid");
        campoPrecio.classList.remove("is-valid");

        return false;

    }

    errorPrecio.textContent = "";

    campoPrecio.classList.remove("is-invalid");
    campoPrecio.classList.add("is-valid");

    return true;

}

function validarCantidad(){

    const cantidad = campoCantidad.value.trim();

    if(cantidad === ""){

        errorCantidad.textContent = "La cantidad es obligatoria.";

        campoCantidad.classList.add("is-invalid");
        campoCantidad.classList.remove("is-valid");

        return false;

    }

    errorCantidad.textContent = "";

    campoCantidad.classList.remove("is-invalid");
    campoCantidad.classList.add("is-valid");

    return true;

}
campoNombre.addEventListener("input", validarNombre);
campoNombre.addEventListener("blur", validarNombre);

campoDescripcion.addEventListener("input", validarDescripcion);
campoDescripcion.addEventListener("blur", validarDescripcion);

campoCategoria.addEventListener("change", validarCategoria);
campoCategoria.addEventListener("blur", validarCategoria);

campoPrecio.addEventListener("input", validarPrecio);
campoPrecio.addEventListener("blur", validarPrecio);

campoCantidad.addEventListener("input", validarCantidad);
campoCantidad.addEventListener("blur", validarCantidad);

formulario.addEventListener("submit", function(event){

    event.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value;
    const precio = campoPrecio.value.trim();
    const cantidad = campoCantidad.value.trim();

    const formularioValido =
    validarNombre() &&
    validarDescripcion() &&
    validarCategoria() &&
    validarPrecio() &&
    validarCantidad();

if(!formularioValido){

mensaje.innerHTML = `
<div class="alert alert-danger d-flex justify-content-center align-items-center text-center" role="alert">

<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
<use xlink:href="#exclamation-triangle-fill"></use>
</svg>

<div>
Corrija los campos antes de registrar el producto.
</div>

</div>
`;

    return;
}
let imagenProducto = "";

switch(categoria){

    case "Vestidos":
        imagenProducto = "/static/img/vestido.jpeg";
        break;

    case "Blusas":
        imagenProducto = "/static/img/blusas.jpeg";
        break;

    case "Jeans":
        imagenProducto = "/static/img/jeans.jpeg";
        break;

    case "Faldas":
        imagenProducto = "/static/img/faldas.jpg";
        break;

    case "Bodys":
        imagenProducto = "/static/img/body.jpg";
        break;

    case "Conjuntos":
        imagenProducto = "/static/img/conjuntos.jpg";
        break;

    case "Chaquetas de mezclilla":
        imagenProducto = "/static/img/chaquetas.jpg";
        break;

    case "Blazers":
        imagenProducto = "/static/img/blazers.jpeg";
        break;

    case "Shorts":
        imagenProducto = "/static/img/shorts.jpeg";
        break;

    case "Enterizos":
        imagenProducto = "/static/img/enterizos.jpg";
        break;

    case "Conjuntos Deportivos":
        imagenProducto = "/static/img/conj_deportivos.png";
        break;

    case "Crop Tops":
        imagenProducto = "/static/img/crop_tops.png";
        break;

    default:
        imagenProducto = "/static/img/modaa.jpeg";
}
    

spinnerCarga.style.display = "block";

mensaje.innerHTML = "";

setTimeout(function(){

spinnerCarga.style.display = "none";

mensaje.innerHTML = `
<div class="alert alert-success d-flex justify-content-center align-items-center text-center" role="alert">

<svg class="bi flex-shrink-0 me-2" width="24" height="24">
<use xlink:href="#check-circle-fill"></use>
</svg>

<div>
Producto registrado correctamente.
</div>

</div>
`;
const modalExito = new bootstrap.Modal(
document.getElementById("modalExito")
);

modalExito.show();
productos.push({

    nombre: nombre,
    categoria: categoria,
    precio: "$" + precio,
    cantidad: cantidad,
    descripcion: descripcion,
    imagen: imagenProducto,

    estado: "Disponible",

    codigo: "PF-" + (productos.length + 1).toString().padStart(3, "0"),

    fecha: new Date().toLocaleDateString("es-EC"),

    observacion: "Producto listo para entrega inmediata."

});

renderizarProductos();

   contadorProductos.textContent = productos.length;

    formulario.reset();

campoNombre.classList.remove("is-valid");
campoDescripcion.classList.remove("is-valid");
campoCategoria.classList.remove("is-valid");
campoPrecio.classList.remove("is-valid");
campoCantidad.classList.remove("is-valid");

errorNombre.textContent = "";
errorDescripcion.textContent = "";
errorCategoria.textContent = "";
errorPrecio.textContent = "";
errorCantidad.textContent = "";

}, 2000);

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
    const soloLetras = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;

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
    if(!soloLetras.test(nombre)){

    errorNombreContacto.textContent = "Solo se permiten letras.";

    campoNombreContacto.classList.add("is-invalid");
    campoNombreContacto.classList.remove("is-valid");

    return false;

}
const partesNombre = nombre.split(/\s+/);

if(partesNombre.length < 2){

    errorNombreContacto.textContent = "Ingrese al menos un nombre y un apellido.";

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
    if(!/[A-Za-zÁÉÍÓÚáéíóúÑñ]/.test(mensaje)){

    errorMensajeContacto.textContent = "Ingrese una consulta válida. Ejemplo: 'Quiero información del vestido talla M'.";

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
<div class="alert alert-danger d-flex justify-content-center align-items-center text-center mt-3" role="alert">

    <svg class="bi flex-shrink-0 me-2" width="24" height="24">
        <use xlink:href="#exclamation-triangle-fill"/>
    </svg>

    <div>
        Corrija los campos antes de enviar el mensaje.
    </div>

</div>
`;

return;
}

mensajeFormulario.innerHTML = `
<div class="alert alert-success d-flex justify-content-center align-items-center text-center mt-3" role="alert">

    <svg class="bi flex-shrink-0 me-2" width="24" height="24">
        <use xlink:href="#check-circle-fill"/>
    </svg>

    <div>
        Mensaje preparado correctamente. Será enviado por WhatsApp.
    </div>

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
function verProducto(indice){

const producto = productos[indice];

document.getElementById("modalImagen").src = producto.imagen;

document.getElementById("modalNombre").textContent = producto.nombre;

document.getElementById("modalCategoria").innerHTML =
"<strong>Categoría:</strong> " + producto.categoria;

document.getElementById("modalPrecio").innerHTML =
"<strong>Precio:</strong> " + producto.precio;

document.getElementById("modalCantidad").innerHTML =
"<strong>Cantidad:</strong> " + producto.cantidad;

document.getElementById("modalDescripcion").innerHTML =
"<strong>Descripción:</strong><br>" + producto.descripcion;
document.getElementById("modalEstado").innerHTML =
"<strong>Estado:</strong> " + producto.estado;

document.getElementById("modalCodigo").innerHTML =
"<strong>Código:</strong> " + producto.codigo;

document.getElementById("modalFecha").innerHTML =
"<strong>Fecha de registro:</strong> " + producto.fecha;

document.getElementById("modalObservacion").innerHTML =
"<strong>Observación:</strong><br>" + producto.observacion;

const modal = new bootstrap.Modal(
document.getElementById("modalProducto")
);

modal.show();

}
// Índice del producto que se desea eliminar
let indiceEliminar = null;
function abrirModalEliminar(indice){

    indiceEliminar = indice;

    const modal = new bootstrap.Modal(
        document.getElementById("modalEliminar")
    );

    modal.show();

}
document.getElementById("btnConfirmarEliminar").addEventListener("click", function(){

    productos.splice(indiceEliminar, 1);

    renderizarProductos();

    contadorProductos.textContent = productos.length;

    const modal = bootstrap.Modal.getInstance(
        document.getElementById("modalEliminar")
    );

    modal.hide();

});

function eliminarProducto(indice){

    if(confirm("¿Está seguro de eliminar este producto?")){

        productos.splice(indice, 1);

        renderizarProductos();

        contadorProductos.textContent = productos.length;

    }

}