import sqlite3 as sql
from sqlite3 import Error
from werkzeug.security import check_password_hash
from flask import g

def crearBD():
    try:
        conn = sql.connect(g.PathBD)
        conn.commit()
        conn.close()
    except Error:
        print(Error)

def crearTabla():
    conn = sql.connect(g.PathBD)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE usuarios(
            nombre text,
            correo text primary key,
            username texto,
            password texto
        )
        """
    )
    conn.commit()
    conn.close()

def insertarElemento(nombre, codigoVenta ,valor, cantidad):
    conn = sql.connect(g.PathBD)
    cursor = conn.cursor()
    instruccion =f"INSERT INTO inventario VALUES('{nombre}',{codigoVenta},{valor},{cantidad})"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def registrarUsuario(nombre, correo, username, password):
    conn = sql.connect(g.PathBD)
    cursor = conn.cursor()
    instruccion = f"INSERT INTO usuarios VALUES('{nombre}','{correo}','{username}','{password}')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def insertarElementos(listadoProductos):
    conn = sql.connect(g.PathBD)
    cursor = conn.cursor()
    instruccion =f"INSERT INTO inventario VALUES(?,?,?)"
    cursor.executemany(instruccion,listadoProductos)
    conn.commit()
    conn.close()

def leerBaseDatos():
    conn = sql.connect (g.PathBD)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM inventario"
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    print(datos)
    conn.commit()
    conn.close()

def buscar(campo, busqueda):
    conn = sql.connect(g.PathBD)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM inventario WHERE {campo} like '{busqueda}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    print(datos)

def actualizarArticulo(nombre,valor):
    conn = sql.connect(g.PathBD)
    cursor = conn.cursor()
    instruccion = f"UPDATE inventario SET valor={valor} WHERE nombre like '{nombre}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def eliminarArticulo(nombre):
    conn = sql.connect(g.PathBD)
    cursor = conn.cursor()
    instruccion = f"DELETE FROM inventario WHERE nombre = '{nombre}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def eliminarTabla(nombreTabla):
    conn = sql.connect(g.PathBD)
    cursor = conn.cursor()
    instruccion = f"DROP TABLE {nombreTabla}"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def validarUsuario(correo,password):
    conn = sql.connect(g.PathBD)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM usuarios WHERE correo='{correo}'"
    cursor.execute(instruccion)
    user=cursor.fetchone()
    passwordUserBD=user[3]
    passwordComparar=check_password_hash(passwordUserBD,password)
    conn.commit()
    conn.close()
    if user is None or passwordComparar is False:
        return False
    else:
        return True

def usuarioSesionActual(correo):
    conn = sql.connect(g.PathBD)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM usuarios WHERE correo='{correo}'"
    cursor.execute(instruccion)
    user=cursor.fetchone()
    conn.commit()
    conn.close()
    return (user)