from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length

class Registro(FlaskForm):
    nombre = StringField ('Nombre ', validators=[
        DataRequired(message="Rellene informacion"),
        Length(min=3, message='Supere los 3 caracteres')
    ])
    correo = EmailField ('Email ', validators=[
        DataRequired(message="Rellene informacion"),
        Email(message='Email invalido')
    ])
    username = StringField('Username: ', validators=[
        DataRequired(message="Ingrese usuario")
    ])
    password = PasswordField ('Pass ', validators=[
        DataRequired(message="Rellene informacion"),
        Length(min=3, message='Supere los 3 caracteres')
    ])
    password2 = PasswordField ('Confirmar Pass', validators=[
        DataRequired(message="Rellene informacion"),
        Length(min=3, message='Supere los 3 caracteres')
    ])
    enviar=SubmitField('Registrarse')


class IngresoProducto(FlaskForm):
    nombre = StringField ('Nombre ', validators=[
        DataRequired(message="Rellene informacion"),
        Length(min=3, message='Supere los 3 caracteres')
    ])
    codigoVenta = StringField('Codigo de Venta: ', validators=[
        DataRequired(message="Rellene informacion"),
        Length(min=3, message='Supere los 3 caracteres')
    ])
    valor = IntegerField ('Valor ', validators=[
        DataRequired(message="Rellene informacion")
    ])
    cantidad = IntegerField ('Cantidad ', validators=[
        DataRequired(message="Rellene informacion")
    ])
    enviar=SubmitField('Ingresar producto')

class Login(FlaskForm):
    correo = EmailField ('Email ', validators=[
        DataRequired(message="Rellene informacion"),
        Email(message='Email invalido')
    ])
    password = PasswordField ('Pass ', validators=[
        DataRequired(message="Rellene informacion"),
        Length(min=3, message='Supere los 3 caracteres')
    ])
    enviar=SubmitField('Ingresar')