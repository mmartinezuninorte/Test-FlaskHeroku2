import json

with open('producto.json') as file:
    datosJson=json.load(file)

productos=datosJson['articulos']
titulo=datosJson['NombreTienda']