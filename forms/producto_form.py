from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre de la Prenda",
        validators=[
            DataRequired(message="El nombre de la prenda es obligatorio."),
            Length(
                min=3,
                max=50,
                message="El nombre debe tener entre 3 y 50 caracteres."
            )
        ]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("", "Seleccione una categoría"),
            ("Vestidos", "Vestidos"),
            ("Blusas", "Blusas"),
            ("Jeans", "Jeans"),
            ("Faldas", "Faldas"),
            ("Bodys", "Bodys"),
            ("Conjuntos", "Conjuntos"),
            ("Chaquetas de mezclilla", "Chaquetas de mezclilla"),
            ("Blazers", "Blazers"),
            ("Shorts", "Shorts"),
            ("Enterizos", "Enterizos"),
            ("Conjuntos Deportivos", "Conjuntos Deportivos"),
            ("Crop Tops", "Crop Tops")
        ],
        validators=[
            DataRequired(message="Seleccione una categoría.")
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            DataRequired(message="La descripción es obligatoria."),
            Length(
                min=10,
                max=200,
                message="La descripción debe tener entre 10 y 200 caracteres."
            )
        ]
    )

    precio = DecimalField(
        "Precio",
        places=2,
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor que 0."
            )
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            InputRequired(message="La cantidad es obligatoria."),
            NumberRange(
                min=0,
                message="La cantidad no puede ser negativa."
            )
        ]
    )

    enviar = SubmitField("Guardar Producto")