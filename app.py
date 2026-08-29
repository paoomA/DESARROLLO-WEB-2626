from flask import Flask, render_template, request, redirect, url_for
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)

# clave secreta para flask-wtf
app.config["SECRET_KEY"] = "paoou-fashion-clave-secreta"

# datos temporales de productos
productos_lista = [
    {
        "nombre": "Vestidos",
        "categoria": "Vestidos",
        "descripcion": "Prenda femenina moderna y elegante.",
        "precio": 25.00,
        "stock": 5
    },
    {
        "nombre": "Blusas",
        "categoria": "Blusas",
        "descripcion": "Diseños modernos en diferentes estilos y colores.",
        "precio": 15.00,
        "stock": 3
    },
    {
        "nombre": "Bodys",
        "categoria": "Bodys",
        "descripcion": "Perfectos para combinar con cualquier look.",
        "precio": 20.00,
        "stock": 0
    }
]

# datos temporales de clientes
clientes_lista = [
    {
        "nombre": "María",
        "apellido": "López",
        "correo": "maria.lopez@gmail.com",
        "telefono": "0991234567",
        "ciudad": "Shushufindi",
        "estado": "Activo"
    },
    {
        "nombre": "Andrea",
        "apellido": "Pérez",
        "correo": "andrea.perez@gmail.com",
        "telefono": "0987654321",
        "ciudad": "Lago Agrio",
        "estado": "Activo"
    },
    {
        "nombre": "Carolina",
        "apellido": "Torres",
        "correo": "carolina.torres@gmail.com",
        "telefono": "0976543210",
        "ciudad": "Quito",
        "estado": "Activo"
    }
]

# datos temporales de proveedores
proveedores_lista = [
    {
        "nombre": "Moda Textil Ecuador",
        "contacto": "Laura Martínez",
        "correo": "modatextil@gmail.com",
        "telefono": "0991234567",
        "producto": "Ropa femenina",
        "estado": "Activo"
    },
    {
        "nombre": "Distribuidora Fashion Style",
        "contacto": "Daniela Torres",
        "correo": "fashionstyle@gmail.com",
        "telefono": "0987654321",
        "producto": "Blusas y vestidos",
        "estado": "Activo"
    },
    {
        "nombre": "Comercial Andina",
        "contacto": "Carlos Mendoza",
        "correo": "comercialandina@gmail.com",
        "telefono": "0976543210",
        "producto": "Jeans y chaquetas",
        "estado": "Activo"
    }
]

# datos temporales de facturación

facturas_lista = [
    {
        "numero_factura": "001-001-000001",
        "fecha": "2026-08-12",
        "cliente": "María López",
        "correo": "maria.lopez@gmail.com",
        "producto": "Vestido Floral Elegante",
        "cantidad": 1,
        "precio": 25.00,
        "estado": "Pagada"
    },
    {
        "numero_factura": "001-001-000002",
        "fecha": "2026-08-13",
        "cliente": "Andrea Pérez",
        "correo": "andrea.perez@gmail.com",
        "producto": "Blusa Casual Elegante",
        "cantidad": 1,
        "precio": 15.00,
        "estado": "Pendiente"
    }
]


# página principal
@app.route("/")
def inicio():
    return render_template("index.html")


# página de productos
@app.route("/productos")
def productos():

    nombre_tienda = "Paoou Fashion"

    return render_template(
        "productos.html",
        nombre_tienda=nombre_tienda,
        productos=productos_lista
    )
# formulario para registrar productos
@app.route("/formulario-producto", methods=["GET", "POST"])
def formulario_producto():

    form = ProductoForm()
    editar = False

    if form.validate_on_submit():

        nuevo_producto = {
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "descripcion": form.descripcion.data,
            "precio": float(form.precio.data),
            "stock": form.cantidad.data
        }

        productos_lista.append(nuevo_producto)

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form,
        editar=editar
    )


# formulario para editar productos
@app.route("/editar-producto/<int:indice>", methods=["GET", "POST"])
def editar_producto(indice):

    if indice < 0 or indice >= len(productos_lista):
        return redirect(url_for("productos"))

    producto = productos_lista[indice]
    form = ProductoForm()
    editar = True

    if request.method == "GET":
        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = producto["precio"]
        form.cantidad.data = producto["stock"]

    if form.validate_on_submit():

        producto["nombre"] = form.nombre.data
        producto["categoria"] = form.categoria.data
        producto["descripcion"] = form.descripcion.data
        producto["precio"] = float(form.precio.data)
        producto["stock"] = form.cantidad.data

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form,
        editar=editar
    )


# eliminar producto
@app.route("/eliminar-producto/<int:indice>")
def eliminar_producto(indice):

    if indice < 0 or indice >= len(productos_lista):
        return redirect(url_for("productos"))

    productos_lista.pop(indice)

    return redirect(url_for("productos"))

# página de clientes

@app.route("/clientes")
def clientes():

    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )


# formulario para registrar clientes
@app.route("/formulario-cliente", methods=["GET", "POST"])
def formulario_cliente():

    form = ClienteForm()
    editar = False

    if form.validate_on_submit():

        nuevo_cliente = {
            "nombre": form.nombre.data,
            "apellido": form.apellido.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data,
            "ciudad": form.ciudad.data,
            "estado": form.estado.data
        }

        clientes_lista.append(nuevo_cliente)

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form,
        editar=editar
    )


# formulario para editar clientes

@app.route("/editar-cliente/<int:indice>", methods=["GET", "POST"])
def editar_cliente(indice):

    if indice < 0 or indice >= len(clientes_lista):
        return redirect(url_for("clientes"))

    cliente = clientes_lista[indice]

    form = ClienteForm()

    editar = True

    if request.method == "GET":

        form.nombre.data = cliente["nombre"]
        form.apellido.data = cliente["apellido"]
        form.correo.data = cliente["correo"]
        form.telefono.data = cliente["telefono"]
        form.ciudad.data = cliente["ciudad"]
        form.estado.data = cliente["estado"]

    if form.validate_on_submit():

        cliente["nombre"] = form.nombre.data
        cliente["apellido"] = form.apellido.data
        cliente["correo"] = form.correo.data
        cliente["telefono"] = form.telefono.data
        cliente["ciudad"] = form.ciudad.data
        cliente["estado"] = form.estado.data

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form,
        editar=editar
    )


# eliminar cliente

@app.route("/eliminar-cliente/<int:indice>")
def eliminar_cliente(indice):

    if indice < 0 or indice >= len(clientes_lista):
        return redirect(url_for("clientes"))

    clientes_lista.pop(indice)

    return redirect(url_for("clientes"))
    
# página de proveedores
@app.route("/proveedores")
def proveedores():

    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )


# formulario para registrar proveedores
@app.route("/formulario-proveedor", methods=["GET", "POST"])
def formulario_proveedor():

    form = ProveedorForm()
    editar = False

    if form.validate_on_submit():

        nuevo_proveedor = {
            "nombre": form.nombre.data,
            "contacto": form.contacto.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data,
            "producto": form.producto.data,
            "estado": form.estado.data
        }

        proveedores_lista.append(nuevo_proveedor)

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form,
        editar=editar
    )


# formulario para editar proveedores
@app.route("/editar-proveedor/<int:indice>", methods=["GET", "POST"])
def editar_proveedor(indice):

    if indice < 0 or indice >= len(proveedores_lista):
        return redirect(url_for("proveedores"))

    proveedor = proveedores_lista[indice]

    form = ProveedorForm()
    editar = True

    if request.method == "GET":

        form.nombre.data = proveedor["nombre"]
        form.contacto.data = proveedor["contacto"]
        form.correo.data = proveedor["correo"]
        form.telefono.data = proveedor["telefono"]
        form.producto.data = proveedor["producto"]
        form.estado.data = proveedor["estado"]

    if form.validate_on_submit():

        proveedor["nombre"] = form.nombre.data
        proveedor["contacto"] = form.contacto.data
        proveedor["correo"] = form.correo.data
        proveedor["telefono"] = form.telefono.data
        proveedor["producto"] = form.producto.data
        proveedor["estado"] = form.estado.data

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form,
        editar=editar
    )


# eliminar proveedor
@app.route("/eliminar-proveedor/<int:indice>")
def eliminar_proveedor(indice):

    if indice < 0 or indice >= len(proveedores_lista):
        return redirect(url_for("proveedores"))

    proveedores_lista.pop(indice)

    return redirect(url_for("proveedores"))


# página de facturación

@app.route("/facturacion")
def facturacion():

    return render_template(
        "facturacion.html",
        facturas=facturas_lista
    )


# formulario para registrar facturas

@app.route("/formulario-facturacion", methods=["GET", "POST"])
def formulario_facturacion():

    form = FacturacionForm()
    editar = False

    if form.validate_on_submit():

        nueva_factura = {
            "numero_factura": form.numero_factura.data,
            "fecha": form.fecha.data,
            "cliente": form.cliente.data,
            "correo": form.correo.data,
            "producto": form.producto.data,
            "cantidad": form.cantidad.data,
            "precio": float(form.precio.data),
            "estado": form.estado.data
        }

        facturas_lista.append(nueva_factura)

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form,
        editar=editar
    )


# formulario para editar facturas

@app.route("/editar-facturacion/<int:indice>", methods=["GET", "POST"])
def editar_facturacion(indice):

    if indice < 0 or indice >= len(facturas_lista):
        return redirect(url_for("facturacion"))

    factura = facturas_lista[indice]

    form = FacturacionForm()

    editar = True

    if request.method == "GET":

        form.numero_factura.data = factura["numero_factura"]
        form.fecha.data = factura["fecha"]
        form.cliente.data = factura["cliente"]
        form.correo.data = factura["correo"]
        form.producto.data = factura["producto"]
        form.cantidad.data = factura["cantidad"]
        form.precio.data = factura["precio"]
        form.estado.data = factura["estado"]

    if form.validate_on_submit():

        factura["numero_factura"] = form.numero_factura.data
        factura["fecha"] = form.fecha.data
        factura["cliente"] = form.cliente.data
        factura["correo"] = form.correo.data
        factura["producto"] = form.producto.data
        factura["cantidad"] = form.cantidad.data
        factura["precio"] = float(form.precio.data)
        factura["estado"] = form.estado.data

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form,
        editar=editar
    )


# eliminar factura

@app.route("/eliminar-facturacion/<int:indice>")
def eliminar_facturacion(indice):

    if indice < 0 or indice >= len(facturas_lista):
        return redirect(url_for("facturacion"))

    facturas_lista.pop(indice)

    return redirect(url_for("facturacion"))


# ejecutar aplicación
if __name__ == "__main__":
    app.run(debug=True)