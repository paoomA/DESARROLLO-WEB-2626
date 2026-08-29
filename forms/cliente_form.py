from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(
                min=3,
                max=30,
                message="El nombre debe tener mínimo 3 caracteres."
            ),
            Regexp(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$",
                message="El nombre solo debe contener letras."
            )
        ]
    )

    apellido = StringField(
        "Apellido",
        validators=[
            DataRequired(message="El apellido es obligatorio."),
            Length(
                min=3,
                max=30,
                message="El apellido debe tener mínimo 3 caracteres."
            ),
            Regexp(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$",
                message="El apellido solo debe contener letras."
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

    ciudad = StringField(
        "Ciudad",
        validators=[
            DataRequired(message="La ciudad es obligatoria."),
            Length(
                min=3,
                max=50,
                message="La ciudad debe tener mínimo 3 caracteres."
            ),
            Regexp(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$",
                message="La ciudad solo debe contener letras."
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

    enviar = SubmitField("Guardar Cliente")