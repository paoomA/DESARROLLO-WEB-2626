from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre del Proveedor",
        validators=[
            DataRequired(message="El nombre del proveedor es obligatorio."),
            Length(
                min=3,
                max=80,
                message="El nombre debe tener entre 3 y 80 caracteres."
            ),
            Regexp(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$",
                message="El nombre solo debe contener letras."
            )
        ]
    )

    contacto = StringField(
        "Persona de Contacto",
        validators=[
            DataRequired(message="La persona de contacto es obligatoria."),
            Length(
                min=3,
                max=50,
                message="El contacto debe tener entre 3 y 50 caracteres."
            ),
            Regexp(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$",
                message="El contacto solo debe contener letras."
            )
        ]
    )

    correo = StringField(
        "Correo Electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Regexp(
                r"^\d{10}$",
                message="El teléfono debe contener exactamente 10 números."
            )
        ]
    )

    producto = StringField(
        "Producto Suministrado",
        validators=[
            DataRequired(message="El producto suministrado es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El producto debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("", "Seleccione un estado"),
            ("Activo", "Activo"),
            ("Inactivo", "Inactivo")
        ],
        validators=[
            DataRequired(message="Seleccione un estado.")
        ]
    )

    enviar = SubmitField("Guardar Proveedor")