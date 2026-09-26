from flask_wtf import FlaskForm

from wtforms import (
    IntegerField,
    DecimalField,
    SubmitField
)

from wtforms.validators import (
    InputRequired,
    NumberRange
)


class DetallePedidoForm(FlaskForm):

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

    producto_id = IntegerField(
        "ID del Producto",
        validators=[
            InputRequired(
                message="El ID del producto es obligatorio."
            ),
            NumberRange(
                min=1,
                message="El ID del producto debe ser mayor que 0."
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
                message="La cantidad debe ser mayor que 0."
            )
        ]
    )

    precio_unitario = DecimalField(
        "Precio Unitario",
        places=2,
        validators=[
            InputRequired(
                message="El precio unitario es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El precio no puede ser negativo."
            )
        ]
    )

    subtotal = DecimalField(
        "Subtotal",
        places=2,
        validators=[
            InputRequired(
                message="El subtotal es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El subtotal no puede ser negativo."
            )
        ]
    )

    enviar = SubmitField(
        "Guardar Detalle"
    )