"""BASE EDUCATIVA INSEGURA. Corregir los TODO antes de la entrega."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "inventario.json"
USUARIOS = RAIZ / "usuarios.json"
LOG = RAIZ / "auditoria.jsonl"


def cargar_inventario():
    # TODO: controlar archivo ausente y JSON inválido. No sobrescribirlos.
    return json.loads(DATOS.read_text(encoding="utf-8"))


def guardar_inventario(productos):
    DATOS.write_text(json.dumps(productos, indent=2), encoding="utf-8")


def registrar_evento(usuario, accion, resultado, **detalles):
    # TODO: guardar un objeto JSON por línea; fecha/hora, usuario, acción,
    # resultado y detalles no sensibles. Nunca guardar contraseña ni hash.
    pass


def autenticar(nombre, clave):
    usuarios = json.loads(USUARIOS.read_text(encoding="utf-8"))
    # TODO: integrar seguridad.py y migrar usuarios.json sin claves legibles.
    for usuario in usuarios:
        if usuario["usuario"] == nombre and usuario["clave"] == clave:
            registrar_evento(nombre, "login", "exitoso")
            return {"usuario": nombre, "rol": usuario["rol"]}
    # TODO: registrar también el intento fallido.
    print("Credenciales incorrectas.")
    return None


def consultar_inventario(sesion):
    # TODO: rechazar si no existe sesión válida.
    productos = cargar_inventario()
    for producto in productos:
        print(producto["id"], producto["nombre"], producto["cantidad"])


def modificar_cantidad(sesion, identificador, entrada):
    # TODO: verificar sesión y rol AQUÍ, antes de modificar.
    # TODO: validar entero entre 0 y 1000, sin interrumpir el programa.
    cantidad = int(entrada)
    productos = cargar_inventario()
    for producto in productos:
        if producto["id"] == identificador:
            anterior = producto["cantidad"]
            producto["cantidad"] = cantidad
            guardar_inventario(productos)
            registrar_evento(
                sesion["usuario"], "modificar", "exitoso",
                producto=identificador, anterior=anterior, nueva=cantidad
            )
            print("Cantidad actualizada.")
            return True
    # TODO: informar identificador inexistente, sin crear productos.
    return False


def main():
    print("Inventario académico — BASE CON DEBILIDADES")
    print("Estudiante:", input("Escriba su nombre: "))
    sesion = None
    while True:
        if sesion is None:
            nombre = input("Usuario (o salir): ")
            if nombre == "salir":
                break
            sesion = autenticar(nombre, input("Contraseña de prueba: "))
            continue
        print("1. Consultar | 2. Modificar | 3. Cerrar sesión | 0. Salir")
        opcion = input("Opción: ")
        if opcion == "1":
            consultar_inventario(sesion)
        elif opcion == "2":
            identificador = input("ID del producto: ")
            entrada = input("Nueva cantidad: ")
            modificar_cantidad(sesion, identificador, entrada)
        elif opcion == "3":
            sesion = None
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
