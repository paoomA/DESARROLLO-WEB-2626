from flask_wtf import FlaskForm

from wtforms import (
    IntegerField,
    SelectField,
    DecimalField,
    SubmitField
)

from wtforms.validators import (
    InputRequired,
    NumberRange,
    DataRequired
)


class PedidoForm(FlaskForm):

    cliente_id = IntegerField(
        "ID del Cliente",
        validators=[
            InputRequired(
                message="El ID del cliente es obligatorio."
            ),
            NumberRange(
                min=1,
                message="El ID del cliente debe ser mayor que 0."
            )
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Pendiente", "Pendiente"),
            ("Procesando", "Procesando"),
            ("Enviado", "Enviado"),
            ("Entregado", "Entregado"),
            ("Pagado", "Pagado"),
            ("Cancelado", "Cancelado")
        ],
        validators=[
            DataRequired(
                message="Seleccione un estado."
            )
        ]
    )

    total = DecimalField(
        "Total",
        places=2,
        validators=[
            InputRequired(
                message="El total es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El total no puede ser negativo."
            )
        ]
    )

    enviar = SubmitField(
        "Guardar Pedido"
    )