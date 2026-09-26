from flask import Flask, render_template, request, redirect, url_for
from datetime import date

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.pedido_form import PedidoForm
from forms.detalle_pedido_form import DetallePedidoForm
from forms.usuario_form import UsuarioForm

from conexion.conexion import obtener_conexion

from io import BytesIO

from flask import send_file

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# clave secreta para flask-wtf
app.config["SECRET_KEY"] = "paoou-fashion-clave-secreta"

# configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

# modelo de usuario para Flask-Login
class Usuario(UserMixin):

    def __init__(self, id, usuario, correo, password, rol):
        self.id = id
        self.usuario = usuario
        self.correo = correo
        self.password = password
        self.rol = rol

# cargar usuario autenticado
@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, usuario, correo, password, rol
        FROM usuarios
        WHERE id = %s
    """, (user_id,))

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario:
        return Usuario(
            usuario[0],
            usuario[1],
            usuario[2],
            usuario[3],
            usuario[4]
        )

    return None


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

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.rol == "admin":
        return redirect(url_for("dashboard_admin"))
    else:
        return redirect(url_for("dashboard_cliente"))


@app.route("/dashboard-admin")
@login_required
def dashboard_admin():
    if current_user.rol != "admin":
        return redirect(url_for("dashboard_cliente"))

    return render_template("dashboard_admin.html")

@app.route("/facturacion")
@login_required
def facturacion():

    if current_user.rol != "admin":
        return redirect(url_for("dashboard_cliente"))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            facturas.id,
            facturas.pedido_id,
            facturas.numero_factura,
            facturas.fecha,
            facturas.estado,
            facturas.subtotal,
            facturas.total,
            facturas.metodo_pago
        FROM facturas
        ORDER BY facturas.id DESC
    """)

    facturas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "facturacion.html",
        facturas=facturas
    )

# marcar factura como pagada
@app.route("/marcar-factura-pagada/<int:id>", methods=["POST"])
@login_required
def marcar_factura_pagada(id):

    if current_user.rol != "admin":
        return redirect(url_for("dashboard_cliente"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Buscar el pedido relacionado con la factura
    cursor.execute("""
        SELECT pedido_id
        FROM facturas
        WHERE id = %s
    """, (id,))

    factura = cursor.fetchone()

    if not factura:
        cursor.close()
        conexion.close()
        return redirect(url_for("facturacion"))

    pedido_id = factura[0]

    # Cambiar la factura a Pagada
    cursor.execute("""
        UPDATE facturas
        SET estado = 'Pagada'
        WHERE id = %s
    """, (id,))

    # Cambiar el pedido a Pagado
    cursor.execute("""
        UPDATE pedidos
        SET estado = 'Pagado'
        WHERE id = %s
    """, (pedido_id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("facturacion"))

@app.route("/dashboard-cliente")
@login_required
def dashboard_cliente():
    if current_user.rol != "cliente":
        return redirect(url_for("dashboard_admin"))

    return render_template("dashboard_cliente.html")

# =========================
# PERFIL DEL USUARIO
# =========================

@app.route("/perfil")
@login_required
def perfil():

    return render_template(
        "perfil.html"
    )


# =========================
# CAMBIAR CONTRASEÑA
# =========================

@app.route("/cambiar-password", methods=["GET", "POST"])
@login_required
def cambiar_password():

    if request.method == "POST":

        password_actual = request.form["password_actual"]
        password_nueva = request.form["password_nueva"]
        repetir_password = request.form["repetir_password"]

        # Verificar contraseña actual
        if not check_password_hash(
            current_user.password,
            password_actual
        ):
            return render_template(
                "cambiar_password.html",
                error="La contraseña actual es incorrecta."
            )

        # Verificar longitud
        if len(password_nueva) < 6:
            return render_template(
                "cambiar_password.html",
                error="La nueva contraseña debe tener al menos 6 caracteres."
            )

        # Verificar coincidencia
        if password_nueva != repetir_password:
            return render_template(
                "cambiar_password.html",
                error="Las nuevas contraseñas no coinciden."
            )

        # Crear nuevo hash
        password_segura = generate_password_hash(
            password_nueva
        )

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE usuarios
            SET password = %s
            WHERE id = %s
        """, (
            password_segura,
            current_user.id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        # Actualizar contraseña en la sesión actual
        current_user.password = password_segura

        return redirect(url_for("perfil"))

    return render_template(
        "cambiar_password.html"
    )    

# registro de usuarios
@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        password_segura = generate_password_hash(
            form.password.data
        )

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # GUARDAR LA CUENTA DE USUARIO
        cursor.execute("""
            INSERT INTO usuarios
            (usuario, correo, password, rol)
            VALUES (%s, %s, %s, %s)
        """, (
            form.usuario.data,
            form.correo.data,
            password_segura,
            "cliente"
        ))

        # GUARDAR AUTOMÁTICAMENTE COMO CLIENTE
        cursor.execute("""
            INSERT INTO clientes
            (nombre, apellido, correo, telefono, ciudad, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            form.usuario.data,
            "",
            form.correo.data,
            form.telefono.data,
            "",
            "Activo"
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )
# =========================
# BUSCAR PRODUCTOS
# =========================

@app.route("/buscar")
@login_required
def buscar():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            categoria,
            descripcion,
            precio,
            cantidad
        FROM productos
    """)

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "buscar.html",
        productos=productos
    )

# ruta catalogo
@app.route("/catalogo")
@login_required
def catalogo():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            categoria,
            descripcion,
            precio,
            cantidad
        FROM productos
        WHERE cantidad > 0
    """)

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "catalogo.html",
        productos=productos
    )

# =========================
# AGREGAR PRODUCTO AL CARRITO
# =========================

@app.route("/agregar-carrito/<int:producto_id>", methods=["POST"])
@login_required
def agregar_carrito(producto_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Buscar producto
    cursor.execute("""
        SELECT id, precio, cantidad
        FROM productos
        WHERE id = %s
    """, (producto_id,))

    producto = cursor.fetchone()

    if not producto or producto[2] <= 0:

        cursor.close()
        conexion.close()

        return redirect(url_for("catalogo"))

    # Buscar carrito activo del usuario
    cursor.execute("""
        SELECT id
        FROM carritos
        WHERE usuario_id = %s
        AND estado = 'Activo'
        LIMIT 1
    """, (current_user.id,))

    carrito = cursor.fetchone()

    # Crear carrito si no existe
    if not carrito:

        cursor.execute("""
            INSERT INTO carritos (usuario_id, estado)
            VALUES (%s, 'Activo')
        """, (current_user.id,))

        carrito_id = cursor.lastrowid

    else:

        carrito_id = carrito[0]


    # Revisar si el producto ya está en el carrito
    cursor.execute("""
        SELECT id, cantidad
        FROM detalle_carrito
        WHERE carrito_id = %s
        AND producto_id = %s
    """, (carrito_id, producto_id))

    detalle = cursor.fetchone()


    if detalle:

        nueva_cantidad = detalle[1] + 1

        # No superar el stock
        if nueva_cantidad <= producto[2]:

            cursor.execute("""
                UPDATE detalle_carrito
                SET cantidad = %s
                WHERE id = %s
            """, (nueva_cantidad, detalle[0]))

    else:

        cursor.execute("""
            INSERT INTO detalle_carrito
            (carrito_id, producto_id, cantidad, precio_unitario)
            VALUES (%s, %s, 1, %s)
        """, (
            carrito_id,
            producto_id,
            producto[1]
        ))


    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("carrito"))


# =========================
# MI CARRITO
# =========================

@app.route("/carrito")
@login_required
def carrito():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            detalle_carrito.id,
            productos.nombre,
            productos.categoria,
            detalle_carrito.cantidad,
            detalle_carrito.precio_unitario,
            detalle_carrito.cantidad * detalle_carrito.precio_unitario AS subtotal,
            productos.cantidad AS stock
        FROM detalle_carrito
        INNER JOIN carritos
            ON detalle_carrito.carrito_id = carritos.id
        INNER JOIN productos
            ON detalle_carrito.producto_id = productos.id
        WHERE carritos.usuario_id = %s
        AND carritos.estado = 'Activo'
    """, (current_user.id,))

    productos_carrito = cursor.fetchall()

    cursor.close()
    conexion.close()

    total = sum(
        producto[5]
        for producto in productos_carrito
    )

    return render_template(
        "carrito.html",
        productos_carrito=productos_carrito,
        total=total
    )

@app.route("/actualizar-carrito/<int:detalle_id>", methods=["POST"])
@login_required
def actualizar_carrito(detalle_id):

    cantidad = int(request.form["cantidad"])

    if cantidad < 1:
        cantidad = 1

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            detalle_carrito.producto_id,
            productos.cantidad
        FROM detalle_carrito
        INNER JOIN productos
            ON detalle_carrito.producto_id = productos.id
        INNER JOIN carritos
            ON detalle_carrito.carrito_id = carritos.id
        WHERE detalle_carrito.id = %s
        AND carritos.usuario_id = %s
    """, (
        detalle_id,
        current_user.id
    ))

    producto = cursor.fetchone()

    if not producto:

        cursor.close()
        conexion.close()

        return redirect(url_for("carrito"))

    stock = producto[1]

    if cantidad > stock:
        cantidad = stock

    cursor.execute("""
        UPDATE detalle_carrito
        SET cantidad = %s
        WHERE id = %s
    """, (
        cantidad,
        detalle_id
    ))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("carrito"))

# =========================
# ELIMINAR DEL CARRITO
# =========================

@app.route("/eliminar-carrito/<int:detalle_id>")
@login_required
def eliminar_carrito(detalle_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE detalle_carrito
        FROM detalle_carrito
        INNER JOIN carritos
            ON detalle_carrito.carrito_id = carritos.id
        WHERE detalle_carrito.id = %s
        AND carritos.usuario_id = %s
    """, (detalle_id, current_user.id))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("carrito"))

# =========================
# REALIZAR PEDIDO
# =========================

@app.route("/realizar-pedido")
@login_required
def realizar_pedido():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id
        FROM carritos
        WHERE usuario_id = %s
        AND estado = 'Activo'
        LIMIT 1
    """, (current_user.id,))

    carrito = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not carrito:

        return redirect(
            url_for("carrito")
        )

    return render_template(
        "tipo_pago.html"
    )



# =========================
# CONFIRMAR PEDIDO
# =========================

@app.route("/confirmar-pedido", methods=["POST"])
@login_required
def confirmar_pedido():

    metodo_pago = request.form["metodo_pago"]

    conexion = obtener_conexion()
    cursor = conexion.cursor()


    # BUSCAR CLIENTE AUTOMÁTICAMENTE

    cursor.execute("""
        SELECT
            id,
            nombre,
            correo,
            telefono,
            ciudad
        FROM clientes
        WHERE correo = %s
        LIMIT 1
    """, (current_user.correo,))

    cliente = cursor.fetchone()


    if not cliente:

        cursor.close()
        conexion.close()

        return (
            "No existe un cliente registrado con el correo "
            "de esta cuenta."
        )


    cliente_id = cliente[0]


    # BUSCAR CARRITO DEL USUARIO

    cursor.execute("""
        SELECT id
        FROM carritos
        WHERE usuario_id = %s
        AND estado = 'Activo'
        LIMIT 1
    """, (current_user.id,))

    carrito = cursor.fetchone()


    if not carrito:

        cursor.close()
        conexion.close()

        return redirect(
            url_for("carrito")
        )


    carrito_id = carrito[0]


    # OBTENER PRODUCTOS DEL CARRITO

    cursor.execute("""
        SELECT
            producto_id,
            cantidad,
            precio_unitario
        FROM detalle_carrito
        WHERE carrito_id = %s
    """, (carrito_id,))

    detalles = cursor.fetchall()


    if not detalles:

        cursor.close()
        conexion.close()

        return redirect(
            url_for("carrito")
        )


    # CREAR PEDIDO

    from datetime import date

    cursor.execute("""
        INSERT INTO pedidos
        (
            cliente_id,
            fecha,
            estado,
            total
        )
        VALUES (%s, %s, %s, %s)
    """, (
        cliente_id,
        date.today(),
        "Pendiente",
        0
    ))

    pedido_id = cursor.lastrowid


    total = 0


    # GUARDAR DETALLE Y DESCONTAR STOCK

    for detalle in detalles:

        producto_id = detalle[0]
        cantidad = detalle[1]
        precio = detalle[2]


        # COMPROBAR STOCK

        cursor.execute("""
            SELECT cantidad
            FROM productos
            WHERE id = %s
        """, (producto_id,))

        stock = cursor.fetchone()


        if not stock or stock[0] < cantidad:

            conexion.rollback()

            cursor.close()
            conexion.close()

            return (
                "No hay suficiente stock disponible "
                "para uno de los productos."
            )


        subtotal = cantidad * precio

        total += subtotal


        cursor.execute("""
            INSERT INTO detalle_pedido
            (
                pedido_id,
                producto_id,
                cantidad,
                precio_unitario,
                subtotal
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            pedido_id,
            producto_id,
            cantidad,
            precio,
            subtotal
        ))


        cursor.execute("""
            UPDATE productos
            SET cantidad = cantidad - %s
            WHERE id = %s
        """, (
            cantidad,
            producto_id
        ))


    # ACTUALIZAR TOTAL DEL PEDIDO

    cursor.execute("""
        UPDATE pedidos
        SET total = %s
        WHERE id = %s
    """, (
        total,
        pedido_id
    ))


    # CREAR FACTURA AUTOMÁTICAMENTE

    numero_factura = "FAC-" + str(pedido_id)


    cursor.execute("""
        INSERT INTO facturas
        (
            pedido_id,
            numero_factura,
            fecha,
            estado,
            subtotal,
            total,
            metodo_pago
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        pedido_id,
        numero_factura,
        date.today(),
        "Pendiente",
        total,
        total,
        metodo_pago
    ))


    # VACIAR CARRITO

    cursor.execute("""
        DELETE FROM detalle_carrito
        WHERE carrito_id = %s
    """, (carrito_id,))


    conexion.commit()

    cursor.close()
    conexion.close()


    return redirect(
        url_for("mis_pedidos")
    )

# =========================
# MIS PEDIDOS
# =========================

@app.route("/mis-pedidos")
@login_required
def mis_pedidos():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            pedidos.id,
            pedidos.fecha,
            pedidos.estado,
            pedidos.total
        FROM pedidos
        INNER JOIN clientes
            ON pedidos.cliente_id = clientes.id
        WHERE clientes.correo = %s
        ORDER BY pedidos.id DESC
    """, (current_user.correo,))

    pedidos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "mis_pedidos.html",
        pedidos=pedidos
    )  

# inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, usuario, correo, password, rol
            FROM usuarios
            WHERE usuario = %s
        """, (usuario,))

        datos_usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if datos_usuario and check_password_hash(
            datos_usuario[3],
            password
        ):

            usuario_actual = Usuario(
                datos_usuario[0],
                datos_usuario[1],
                datos_usuario[2],
                datos_usuario[3],
                datos_usuario[4]
            )

            login_user(usuario_actual)

            if usuario_actual.rol == "admin":
                return redirect(url_for("dashboard_admin"))
            else:
                return redirect(url_for("dashboard_cliente"))

        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos."
        )

    return render_template("login.html")

# cerrar sesión
@app.route("/logout")
def logout():

    logout_user()

    return redirect(url_for("inicio"))    


# página de productos
@app.route("/productos")
@login_required
def productos():

    nombre_tienda = "Paoou Fashion"

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            categoria,
            descripcion,
            precio,
            cantidad
        FROM productos
    """)

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        nombre_tienda=nombre_tienda,
        productos=productos
    )


# formulario para registrar productos
@app.route("/formulario-producto", methods=["GET", "POST"])
@login_required
def formulario_producto():

    form = ProductoForm()
    editar = False

    # registrar producto
    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO productos
            (nombre, categoria, descripcion, precio, cantidad)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.descripcion.data,
            float(form.precio.data),
            form.cantidad.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form,
        editar=editar
    )


# formulario para editar productos
@app.route("/editar-producto/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    # buscar producto
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            categoria,
            descripcion,
            precio,
            cantidad
        FROM productos
        WHERE id = %s
    """, (id,))

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    if producto is None:
        return redirect(url_for("productos"))

    form = ProductoForm()
    editar = True

    # cargar datos actuales en el formulario
    if request.method == "GET":

        form.nombre.data = producto[1]
        form.categoria.data = producto[2]
        form.descripcion.data = producto[3]
        form.precio.data = producto[4]
        form.cantidad.data = producto[5]

    # actualizar producto
    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE productos
            SET
                nombre = %s,
                categoria = %s,
                descripcion = %s,
                precio = %s,
                cantidad = %s
            WHERE id = %s
        """, (
            form.nombre.data,
            form.categoria.data,
            form.descripcion.data,
            float(form.precio.data),
            form.cantidad.data,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form,
        editar=editar
    )


# eliminar producto
@app.route("/eliminar-producto/<int:id>")
@login_required
def eliminar_producto(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM productos WHERE id = %s",
        (id,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("productos"))   

# página de clientes
@app.route("/clientes")
@login_required
def clientes():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nombre, apellido, correo, telefono, ciudad, estado
        FROM clientes
        ORDER BY id ASC
    """)

    clientes_lista = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )


# formulario para registrar clientes
@app.route("/formulario-cliente", methods=["GET", "POST"])
@login_required
def formulario_cliente():

    form = ClienteForm()
    editar = False

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (nombre, apellido, correo, telefono, ciudad, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.apellido.data,
            form.correo.data,
            form.telefono.data,
            form.ciudad.data,
            form.estado.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form,
        editar=editar
    )


# formulario para editar clientes
@app.route("/editar-cliente/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nombre, apellido, correo, telefono, ciudad, estado
        FROM clientes
        WHERE id = %s
    """, (id,))

    cliente = cursor.fetchone()

    cursor.close()
    conexion.close()

    if cliente is None:
        return redirect(url_for("clientes"))

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

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE clientes
            SET nombre = %s,
                apellido = %s,
                correo = %s,
                telefono = %s,
                ciudad = %s,
                estado = %s
            WHERE id = %s
        """, (
            form.nombre.data,
            form.apellido.data,
            form.correo.data,
            form.telefono.data,
            form.ciudad.data,
            form.estado.data,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form,
        editar=editar
    )


# eliminar cliente
@app.route("/eliminar-cliente/<int:id>")
@login_required
def eliminar_cliente(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id = %s
    """, (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("clientes"))
    
# página de proveedores
@app.route("/proveedores")
@login_required
def proveedores():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nombre, contacto, correo, telefono, producto, estado
        FROM proveedores
        ORDER BY id ASC
    """)

    proveedores_lista = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )


# formulario para registrar proveedores
@app.route("/formulario-proveedor", methods=["GET", "POST"])
@login_required
def formulario_proveedor():

    form = ProveedorForm()
    editar = False

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (nombre, contacto, correo, telefono, producto, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.contacto.data,
            form.correo.data,
            form.telefono.data,
            form.producto.data,
            form.estado.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form,
        editar=editar
    )


# formulario para editar proveedores
@app.route("/editar-proveedor/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nombre, contacto, correo, telefono, producto, estado
        FROM proveedores
        WHERE id = %s
    """, (id,))

    proveedor = cursor.fetchone()

    cursor.close()
    conexion.close()

    if proveedor is None:
        return redirect(url_for("proveedores"))

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

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                contacto = %s,
                correo = %s,
                telefono = %s,
                producto = %s,
                estado = %s
            WHERE id = %s
        """, (
            form.nombre.data,
            form.contacto.data,
            form.correo.data,
            form.telefono.data,
            form.producto.data,
            form.estado.data,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form,
        editar=editar
    )


# eliminar proveedor
@app.route("/eliminar-proveedor/<int:id>")
@login_required
def eliminar_proveedor(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM proveedores
        WHERE id = %s
    """, (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("proveedores"))

# página de facturación

@app.route("/mis-facturas")
@login_required
def mis_facturas():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            facturas.id,
            facturas.numero_factura,
            facturas.fecha,
            facturas.estado,
            facturas.subtotal,
            facturas.total,
            facturas.metodo_pago,
            pedidos.id
        FROM facturas
        INNER JOIN pedidos
            ON facturas.pedido_id = pedidos.id
        INNER JOIN clientes
            ON pedidos.cliente_id = clientes.id
        WHERE clientes.correo = %s
        ORDER BY facturas.id DESC
    """, (current_user.correo,))

    facturas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "mis_facturas.html",
        facturas=facturas
    )

# =========================
# DETALLE DE FACTURA
# =========================

@app.route("/factura/<int:factura_id>")
@login_required
def detalle_factura(factura_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # DATOS DE LA FACTURA Y DEL CLIENTE

    cursor.execute("""
        SELECT
            facturas.id,
            facturas.numero_factura,
            facturas.fecha,
            facturas.estado,
            facturas.subtotal,
            facturas.total,
            facturas.metodo_pago,
            pedidos.id,
            clientes.nombre,
            clientes.correo,
            clientes.telefono,
            clientes.ciudad
        FROM facturas
        INNER JOIN pedidos
            ON facturas.pedido_id = pedidos.id
        INNER JOIN clientes
            ON pedidos.cliente_id = clientes.id
        WHERE facturas.id = %s
        AND clientes.correo = %s
    """, (
        factura_id,
        current_user.correo
    ))

    factura = cursor.fetchone()

    if not factura:

        cursor.close()
        conexion.close()

        return redirect(
            url_for("mis_facturas")
        )

    # PRODUCTOS DE LA FACTURA

    cursor.execute("""
        SELECT
            productos.nombre,
            productos.categoria,
            detalle_pedido.cantidad,
            detalle_pedido.precio_unitario,
            detalle_pedido.subtotal
        FROM detalle_pedido
        INNER JOIN productos
            ON detalle_pedido.producto_id = productos.id
        WHERE detalle_pedido.pedido_id = %s
    """, (factura[7],))

    detalles = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "detalle_factura.html",
        factura=factura,
        detalles=detalles
    )

# =========================
# DESCARGAR FACTURA PDF
# =========================

@app.route("/factura/<int:factura_id>/pdf")
@login_required
def descargar_factura_pdf(factura_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # DATOS DE FACTURA Y CLIENTE

    cursor.execute("""
        SELECT
            facturas.id,
            facturas.numero_factura,
            facturas.fecha,
            facturas.estado,
            facturas.subtotal,
            facturas.total,
            facturas.metodo_pago,
            pedidos.id,
            clientes.nombre,
            clientes.correo,
            clientes.telefono,
            clientes.ciudad
        FROM facturas
        INNER JOIN pedidos
            ON facturas.pedido_id = pedidos.id
        INNER JOIN clientes
            ON pedidos.cliente_id = clientes.id
        WHERE facturas.id = %s
        AND clientes.correo = %s
    """, (
        factura_id,
        current_user.correo
    ))

    factura = cursor.fetchone()

    if not factura:

        cursor.close()
        conexion.close()

        return redirect(
            url_for("mis_facturas")
        )


    # PRODUCTOS

    cursor.execute("""
        SELECT
            productos.nombre,
            productos.categoria,
            detalle_pedido.cantidad,
            detalle_pedido.precio_unitario,
            detalle_pedido.subtotal
        FROM detalle_pedido
        INNER JOIN productos
            ON detalle_pedido.producto_id = productos.id
        WHERE detalle_pedido.pedido_id = %s
    """, (factura[7],))

    detalles = cursor.fetchall()

    cursor.close()
    conexion.close()


    # CREAR PDF

    archivo = BytesIO()

    documento = SimpleDocTemplate(
        archivo,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    estilos = getSampleStyleSheet()

    contenido = []


    # TÍTULO

    contenido.append(
        Paragraph(
            "<b>PAOOU FASHION</b>",
            estilos["Title"]
        )
    )

    contenido.append(
        Paragraph(
            "FACTURA DE VENTA",
            estilos["Heading2"]
        )
    )

    contenido.append(Spacer(1, 15))


    # DATOS DE FACTURA

    datos_factura = [
        [
            "Número de factura:",
            str(factura[1])
        ],
        [
            "Fecha:",
            str(factura[2])
        ],
        [
            "Estado:",
            str(factura[3])
        ]
    ]

    tabla_factura = Table(
        datos_factura,
        colWidths=[150, 300]
    )

    tabla_factura.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.whitesmoke
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            )
        ])
    )

    contenido.append(tabla_factura)

    contenido.append(Spacer(1, 20))


    # CLIENTE

    contenido.append(
        Paragraph(
            "<b>DATOS DEL CLIENTE</b>",
            estilos["Heading3"]
        )
    )

    datos_cliente = [
        ["Nombre:", str(factura[8])],
        ["Correo:", str(factura[9])],
        ["Teléfono:", str(factura[10])],
        ["Ciudad:", str(factura[11])]
    ]

    tabla_cliente = Table(
        datos_cliente,
        colWidths=[100, 350]
    )

    tabla_cliente.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            )
        ])
    )

    contenido.append(tabla_cliente)

    contenido.append(Spacer(1, 20))


    # PRODUCTOS

    contenido.append(
        Paragraph(
            "<b>DETALLE DE PRODUCTOS</b>",
            estilos["Heading3"]
        )
    )


    datos_productos = [
        [
            "Producto",
            "Categoría",
            "Cantidad",
            "Precio",
            "Subtotal"
        ]
    ]


    for detalle in detalles:

        datos_productos.append([
            str(detalle[0]),
            str(detalle[1]),
            str(detalle[2]),
            "$%.2f" % float(detalle[3]),
            "$%.2f" % float(detalle[4])
        ])


    tabla_productos = Table(
        datos_productos,
        colWidths=[
            130,
            100,
            60,
            70,
            80
        ]
    )


    tabla_productos.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#e889ad")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "ALIGN",
                (2, 1),
                (-1, -1),
                "CENTER"
            )
        ])
    )


    contenido.append(tabla_productos)

    contenido.append(Spacer(1, 20))


    # TOTALES

    datos_totales = [
        [
            "Subtotal:",
            "$%.2f" % float(factura[4])
        ],
        [
            "TOTAL:",
            "$%.2f" % float(factura[5])
        ],
        [
            "Método de pago:",
            str(factura[6])
        ]
    ]


    tabla_totales = Table(
        datos_totales,
        colWidths=[150, 150],
        hAlign="RIGHT"
    )


    tabla_totales.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTNAME",
                (0, 1),
                (-1, 1),
                "Helvetica-Bold"
            )
        ])
    )


    contenido.append(tabla_totales)

    contenido.append(Spacer(1, 25))


    contenido.append(
        Paragraph(
            "Gracias por comprar en PAOOU FASHION.",
            estilos["Normal"]
        )
    )


    documento.build(contenido)

    archivo.seek(0)


    return send_file(
        archivo,
        as_attachment=True,
        download_name=f"Factura_{factura[1]}.pdf",
        mimetype="application/pdf"
    )    

# formulario para registrar facturas

@app.route("/formulario-facturacion", methods=["GET", "POST"])
@login_required
def formulario_facturacion():

    form = FacturacionForm()
    editar = False

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO facturas
            (
                pedido_id,
                numero_factura,
                fecha,
                estado,
                subtotal,
                total
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            form.pedido_id.data,
            form.numero_factura.data,
            form.fecha.data,
            form.estado.data,
            form.subtotal.data,
            form.total.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form,
        editar=editar
    )


# formulario para editar facturas

@app.route("/editar-facturacion/<int:id>", methods=["GET", "POST"])
@login_required
def editar_facturacion(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id,
               pedido_id,
               numero_factura,
               fecha,
               estado,
               subtotal,
               total
        FROM facturas
        WHERE id = %s
    """, (id,))

    factura = cursor.fetchone()

    cursor.close()
    conexion.close()

    if factura is None:
        return redirect(url_for("facturacion"))

    form = FacturacionForm()
    editar = True

    if request.method == "GET":

        form.pedido_id.data = factura["pedido_id"]
        form.numero_factura.data = factura["numero_factura"]
        form.fecha.data = factura["fecha"]
        form.estado.data = factura["estado"]
        form.subtotal.data = factura["subtotal"]
        form.total.data = factura["total"]

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE facturas
            SET pedido_id = %s,
                numero_factura = %s,
                fecha = %s,
                estado = %s,
                subtotal = %s,
                total = %s
            WHERE id = %s
        """, (
            form.pedido_id.data,
            form.numero_factura.data,
            form.fecha.data,
            form.estado.data,
            form.subtotal.data,
            form.total.data,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form,
        editar=editar
    )


# eliminar factura

@app.route("/eliminar-facturacion/<int:id>")
@login_required
def eliminar_facturacion(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM facturas
        WHERE id = %s
    """, (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("facturacion"))

# =========================================================
# PEDIDOS
# =========================================================

@app.route("/pedidos")
@login_required
def pedidos():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            pedidos.id,
            pedidos.cliente_id,
            clientes.nombre AS nombre_cliente,
            pedidos.fecha,
            pedidos.estado,
            pedidos.total
        FROM pedidos
        INNER JOIN clientes
            ON pedidos.cliente_id = clientes.id
        ORDER BY pedidos.id ASC
    """)

    pedidos_lista = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "pedidos.html",
        pedidos=pedidos_lista
    )


# =========================================================
# FORMULARIO PARA REGISTRAR PEDIDOS
# =========================================================

@app.route("/formulario_pedido", methods=["GET", "POST"])
@login_required
def formulario_pedido():

    form = PedidoForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO pedidos (
                cliente_id,
                fecha,
                estado,
                total
            )
            VALUES (%s, %s, %s, %s)
        """, (
            form.cliente_id.data,
            date.today(),
            form.estado.data,
            form.total.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("pedidos"))

    return render_template(
        "formulario_pedido.html",
        form=form
    )

# =========================================================
# EDITAR PEDIDO
# =========================================================

@app.route("/editar-pedido/<int:id>", methods=["GET", "POST"])
@login_required
def editar_pedido(id):

    if current_user.rol != "admin":
        return redirect(url_for("dashboard_cliente"))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            cliente_id,
            fecha,
            estado,
            total
        FROM pedidos
        WHERE id = %s
    """, (id,))

    pedido = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not pedido:
        return redirect(url_for("pedidos"))

    form = PedidoForm()

    if request.method == "GET":

        form.cliente_id.data = pedido["cliente_id"]
        form.estado.data = pedido["estado"]
        form.total.data = pedido["total"]

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE pedidos
            SET cliente_id = %s,
                estado = %s,
                total = %s
            WHERE id = %s
        """, (
            form.cliente_id.data,
            form.estado.data,
            form.total.data,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("pedidos"))

    return render_template(
        "formulario_pedido.html",
        form=form,
        editar=True
    )


# =========================================================
# ELIMINAR PEDIDO
# =========================================================

@app.route("/eliminar-pedido/<int:id>")
@login_required
def eliminar_pedido(id):

    if current_user.rol != "admin":
        return redirect(url_for("dashboard_cliente"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM pedidos
        WHERE id = %s
    """, (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("pedidos"))

# =========================================================
# ACTUALIZAR ESTADO DEL PEDIDO AUTOMÁTICAMENTE
# =========================================================

@app.route("/actualizar-estado-pedido/<int:id>", methods=["POST"])
@login_required
def actualizar_estado_pedido(id):

    if current_user.rol != "admin":
        return redirect(url_for("dashboard_cliente"))

    estado = request.form.get("estado")

    estados_permitidos = [
        "Pendiente",
        "Procesando",
        "Enviado",
        "Entregado",
        "Pagado",
        "Cancelado"
    ]

    if estado not in estados_permitidos:
        return redirect(url_for("pedidos"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE pedidos
        SET estado = %s
        WHERE id = %s
    """, (
        estado,
        id
    ))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("pedidos"))

# =========================================================
# DETALLE_PEDIDO
# =========================================================
@app.route("/detalle_pedido")
@login_required
def detalle_pedido():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            pedido_id,
            producto_id,
            cantidad,
            precio_unitario,
            subtotal
        FROM detalle_pedido
        ORDER BY id ASC
    """)

    detalles_lista = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "detalle_pedido.html",
        detalles=detalles_lista
    )

# =========================================================
# FORMULARIO PARA REGISTRAR DETALLE_PEDIDO
# =========================================================

@app.route("/formulario_detalle_pedido", methods=["GET", "POST"])
@login_required
def formulario_detalle_pedido():

    formulario = DetallePedidoForm()

    if formulario.validate_on_submit():

        pedido_id = formulario.pedido_id.data
        producto_id = formulario.producto_id.data
        cantidad = formulario.cantidad.data
        precio_unitario = formulario.precio_unitario.data
        subtotal = formulario.subtotal.data

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO detalle_pedido
            (
                pedido_id,
                producto_id,
                cantidad,
                precio_unitario,
                subtotal
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            pedido_id,
            producto_id,
            cantidad,
            precio_unitario,
            subtotal
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("detalle_pedido"))

    return render_template(
        "formulario_detalle_pedido.html",
        formulario=formulario
    )

# USUARIO
@app.route("/usuarios")
@login_required
def usuarios():

    if current_user.rol != "admin":
        return redirect(url_for("dashboard_cliente"))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            usuario,
            correo,
            rol
        FROM usuarios
        ORDER BY id ASC
    """)

    usuarios_lista = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "usuarios.html",
        usuarios=usuarios_lista
    )

# prueba de conexión con MySQL
@app.route("/test_db")
def test_db():

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()

        return f"""
            <h2>Conexión exitosa con MySQL</h2>
            <p>Tablas encontradas:</p>
            <p>{tablas}</p>
        """

    except Exception as error:

        return f"""
            <h2>Error de conexión con MySQL</h2>
            <p>{error}</p>
        """

    finally:

        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


# ejecutar aplicación
if __name__ == "__main__":
    app.run(debug=True)