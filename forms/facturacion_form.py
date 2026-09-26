from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SelectField,
    IntegerField,
    DecimalField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange
)


class FacturacionForm(FlaskForm):

    pedido_id = IntegerField(
        "ID del Pedido",
        validators=[
            InputRequired(
                message="El ID del pedido es obligatorio."
            ),
            NumberRange(
                min=1,
                message="El ID del pedido debe ser mayor que 0."
            )
        ]
    )

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

    subtotal = DecimalField(
        "Subtotal",
        places=2,
        validators=[
            DataRequired(
                message="El subtotal es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El subtotal no puede ser negativo."
            )
        ]
    )

    total = DecimalField(
        "Total",
        places=2,
        validators=[
            DataRequired(
                message="El total es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El total no puede ser negativo."
            )
        ]
    )

    enviar = SubmitField(
        "Guardar Factura"
    )