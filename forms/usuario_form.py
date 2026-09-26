from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class UsuarioForm(FlaskForm):

    usuario = StringField(
        "Usuario",
        validators=[
            DataRequired(message="El usuario es obligatorio."),
            Length(
                min=3,
                max=50,
                message="El usuario debe tener entre 3 y 50 caracteres."
            )
        ]
    )

    correo = StringField(
        "Correo",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(
                min=7,
                max=10,
                message="El teléfono debe tener entre 7 y 10 números."
            ),
            Regexp(
                r"^[0-9]+$",
                message="El teléfono solo puede contener números."
            )
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(
                min=6,
                max=255,
                message="La contraseña debe tener al menos 6 caracteres."
            )
        ]
    )

    repetir_password = PasswordField(
        "Repetir contraseña",
        validators=[
            DataRequired(message="Debe repetir la contraseña."),
            EqualTo(
                "password",
                message="Las contraseñas no coinciden."
            )
        ]
    )

    submit = SubmitField("Crear cuenta")