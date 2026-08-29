from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DecimalField, SubmitField
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
    Email,
    Regexp
)


class FacturacionForm(FlaskForm):

    numero_factura = StringField(
        "Número de Factura",
        validators=[
            DataRequired(
                message="El número de factura es obligatorio."
            ),
            Length(
                min=3,
                max=30,
                message="El número de factura debe tener entre 3 y 30 caracteres."
            )
        ]
    )

    fecha = StringField(
        "Fecha",
        validators=[
            DataRequired(
                message="La fecha es obligatoria."
            )
        ]
    )

    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired(
                message="El nombre del cliente es obligatorio."
            ),
            Length(
                min=3,
                max=80,
                message="El nombre del cliente debe tener entre 3 y 80 caracteres."
            ),
            Regexp(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$",
                message="El nombre del cliente solo debe contener letras."
            )
        ]
    )

    correo = StringField(
        "Correo Electrónico",
        validators=[
            DataRequired(
                message="El correo electrónico es obligatorio."
            ),
            Email(
                message="Ingrese un correo electrónico válido."
            )
        ]
    )

    producto = StringField(
        "Producto",
        validators=[
            DataRequired(
                message="El producto es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El producto debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            InputRequired(
                message="La cantidad es obligatoria."
            ),
            NumberRange(
                min=1,
                message="La cantidad debe ser mínimo 1."
            )
        ]
    )

    precio = DecimalField(
        "Precio",
        places=2,
        validators=[
            DataRequired(
                message="El precio es obligatorio."
            ),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor que 0."
            )
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("", "Seleccione un estado"),
            ("Pendiente", "Pendiente"),
            ("Pagada", "Pagada"),
            ("Anulada", "Anulada")
        ],
        validators=[
            DataRequired(
                message="Seleccione un estado."
            )
        ]
    )

    enviar = SubmitField(
        "Guardar Factura"
    )