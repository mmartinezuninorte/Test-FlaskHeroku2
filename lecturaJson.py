import json

with open('producto.json') as file:
    datosJson=json.load(file)

articulosJson=datosJson['articulos']

print(articulosJson[0])