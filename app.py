from flask import Flask, make_response, render_template, jsonify, flash, url_for, redirect, g, session
from formularios import IngresoProducto, Registro, Login
from productos import productos, titulo
import os
from baseDatos import insertarElemento, registrarUsuario,  validarUsuario, usuarioSesionActual
from werkzeug.security import generate_password_hash
import functools


app=Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    name=titulo
    return render_template('index.html', name=name)

@app.before_request
def cargarUsuarioLogueado():
    #config
    g.pathBD='productos.db'
    #ObtenerUsuarioActual
    user_id=session.get('user_id')
    if user_id is None:
        g.user= None
    else:
        g.user = usuarioSesionActual(user_id)

@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesion de manera correcta")
    return redirect(url_for('login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Para acceder a este modulo necesitas estar logueado")
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view


@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    form=Registro()
    nombre=form.nombre.data
    username=form.username.data
    correo=form.correo.data
    password=form.password.data
    password2=form.password2.data
    if (form.validate_on_submit()):
        if (password == password2):

            passwordHash=generate_password_hash(password)
            registrarUsuario(nombre,correo,username,passwordHash)

        else:
            flash ('Contraseñas no coinciden')
            return render_template('registro.html', form=form)
    return render_template('registro.html', form=form)


@app.route('/login/', methods=['GET',"POST"])
def login():
    form=Login()
    try:
        if g.user:
            flash("Ya tienes una sesion iniciada!")
            return redirect ( url_for('ingreseProducto'))
        if (form.validate_on_submit()):
            try:
                correo=form.correo.data
                password=form.password.data
                comprobacion=validarUsuario(correo,password)
                if comprobacion:
                    session.clear()
                    session['user_id']=correo
                    resp= make_response(redirect(url_for('ingreseProducto')))
                    resp.set_cookie('username',correo)
                    flash('Inicio de sesion exitoso')
                    return resp
                else:
                    flash ('Email o password incorrectos')
                    return render_template ('login.html', form=form) 
            except:
                flash ("Opps algo salio mal, intenta eliminar cookies y recargar la pagina ")
                return render_template ('login.html', form=form)
        return render_template('login.html', form=form)
    except:
        flash("Opps algo salio mal al intentar verificar tu sesion, contacta con soporte")
        return render_template('login.html', form=form)

@app.route('/ingresarProductos/', methods=['GET','POST'])
@login_required
def ingreseProducto():
    try:
        form=IngresoProducto()
        nombre=form.nombre.data
        valor=form.valor.data
        cantidad=form.cantidad.data
        codigoVenta=form.codigoVenta.data
        if (form.validate_on_submit()):
            insertarElemento(nombre,codigoVenta,valor,cantidad)
            return render_template('ingresarProductos.html',form=form)
        return render_template('ingresarProductos.html',form=form)
    except:
        return render_template('errorProducto.html')
    

@app.route('/api/')
def api():
    return jsonify({'articulos':productos,'message':"Este es el listado de productos"})

@app.route('/api/<string:nomproducto>')
def buscarArticulo(nomproducto):
    buscador=[producto for producto in productos if producto['nombre']==nomproducto]
    if (len(buscador)>0):
        return jsonify({"producto": buscador[0]})
    return jsonify({"message":"Producto no encontrado"})


if __name__=='__main__':
    app.run(debug=True, ssl_context=('server.cer','server.key'))