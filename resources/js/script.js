const formulario = document.getElementById("formProducto");
const mensaje = document.getElementById("mensaje");
const listaProductos = document.getElementById("listaProductos");
const contadorProductos = document.getElementById("contadorProductos");

let totalProductos = 0;

formulario.addEventListener("submit", function(event){

    event.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value.trim();

    if(nombre === "" || descripcion === "" || categoria === ""){

        mensaje.innerHTML = `
        <div class="alert alert-danger">
            Todos los campos son obligatorios.
        </div>
        `;

        return;
    }

    mensaje.innerHTML = `
    <div class="alert alert-success">
        Producto registrado correctamente.
    </div>
    `;

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

        tarjeta.remove();

        totalProductos--;

        contadorProductos.textContent = totalProductos;

    });

    tarjeta.appendChild(botonEliminar);

    listaProductos.appendChild(tarjeta);

    totalProductos++;

    contadorProductos.textContent = totalProductos;

    formulario.reset();

});

const formContacto = document.getElementById("formContacto");
const mensajeFormulario = document.getElementById("respuestaContacto");

formContacto.addEventListener("submit", function(event){

    event.preventDefault();

    const nombre = document.getElementById("nombreContacto").value.trim();
    const correo = document.getElementById("correoContacto").value.trim();
    const tipo = document.getElementById("tipoConsulta").value;
    const mensaje = document.getElementById("mensajeContacto").value.trim();

    if(nombre === "" || correo === "" || tipo === "" || mensaje === ""){

        mensajeFormulario.innerHTML = `
        <div class="alert alert-danger mt-3">
            Complete todos los campos del formulario.
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

setTimeout(function(){

    document.getElementById("respuestaContacto").innerHTML = "";

}, 3000);

});