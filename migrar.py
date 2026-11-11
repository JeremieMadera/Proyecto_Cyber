import json
from seguridad import crear_hash

with open("usuarios.json", encoding="utf-8") as archivo:
    usuarios = json.load(archivo)

for usuario in usuarios:
    usuario["hash"] = crear_hash(usuario["clave"])
    del usuario["clave"]

with open("usuarios.json", "w", encoding="utf-8") as archivo:
    json.dump(usuarios, archivo, indent=2)