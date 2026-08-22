from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal
@app.route("/")
def inicio():
    return render_template("index.html")

# Ruta del módulo Productos
@app.route("/productos")
def productos():

    nombre_tienda = "Paoou Fashion"

    productos = [
        {
            "nombre": "Vestidos",
            "precio": 25.00,
            "stock": 5
        },
        {
            "nombre": "Blusas",
            "precio": 15.00,
            "stock": 3
        },
        {
            "nombre": "Bodys",
            "precio": 20.00,
            "stock": 0
        }
    ]

    return render_template(
        "productos.html",
        nombre_tienda=nombre_tienda,
        productos=productos
    )

# Ruta del módulo Clientes
@app.route("/clientes")
def clientes():

    clientes = [
        {
            "nombre": "María López",
            "correo": "maria.lopez@gmail.com",
            "telefono": "0991234567",
            "ciudad": "Shushufindi",
            "estado": "Activo"
        },
        {
            "nombre": "Andrea Pérez",
            "correo": "andrea.perez@gmail.com",
            "telefono": "0987654321",
            "ciudad": "Lago Agrio",
            "estado": "Activo"
        },
        {
            "nombre": "Carolina Torres",
            "correo": "carolina.torres@gmail.com",
            "telefono": "0976543210",
            "ciudad": "Quito",
            "estado": "Activo"
        }
    ]

    return render_template(
        "clientes.html",
        clientes=clientes
    )

# Ruta del módulo Proveedores
@app.route("/proveedores")
def proveedores():

    proveedores = [
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

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    ) 

# Ruta de módulo Facturación
@app.route("/facturacion")
def facturacion():
    return render_template("facturacion.html")

if __name__ == "__main__":
    app.run(debug=True)