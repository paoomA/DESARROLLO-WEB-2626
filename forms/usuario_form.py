from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class UsuarioForm(FlaskForm):

    usuario = StringField(
        "Usuario",
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            Regexp(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$",
                message="El nombre solo debe contener letras."
            )
        ]
    )

    apellido = StringField(
        "Apellido",
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            Regexp(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$",
                message="El apellido solo debe contener letras."
            )
        ]
    )

    correo = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{10}$",
                message="El teléfono debe contener exactamente 10 números."
            )
        ]
    )

    ciudad = StringField(
        "Ciudad",
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$",
                message="La ciudad solo debe contener letras."
            )
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(min=6, max=255)
        ]
    )

    repetir_password = PasswordField(
        "Repite tu contraseña",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Las contraseñas no coinciden."
            )
        ]
    )

    submit = SubmitField("Crear cuenta")