"""BASE EDUCATIVA INSEGURA. Corregir los TODO antes de la entrega."""
import json
from datetime import datetime, timezone
from pathlib import Path
from seguridad import verificar_clave

RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "inventario.json"
USUARIOS = RAIZ / "usuarios.json"
LOG = RAIZ / "auditoria.jsonl"


def cargar_inventario():
    try:
        return json.loads(DATOS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("No se encontró el archivo de inventario.")
        return []
    except json.JSONDecodeError:
        print("El archivo de inventario no contiene JSON válido.")
        return []


def guardar_inventario(productos):
    DATOS.write_text(json.dumps(productos, indent=2), encoding="utf-8")


def registrar_evento(usuario, accion, resultado, **detalles):
    evento = {
        "fecha": datetime.now(timezone.utc).isoformat(),
        "usuario": usuario,
        "accion": accion,
        "resultado": resultado,
        "detalles": detalles,
    }
    with LOG.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(evento, ensure_ascii=True) + "\n")


def autenticar(nombre, clave):
    usuarios = json.loads(USUARIOS.read_text(encoding="utf-8"))
    
    for usuario in usuarios:
        if usuario["usuario"] == nombre and verificar_clave(usuario["hash"], clave):
            registrar_evento(nombre, "login", "exitoso")
            return {"usuario": nombre, "rol": usuario["rol"]}
    
    registrar_evento(nombre, "login", "fallido")
    print("Credenciales incorrectas.")
    return None


def consultar_inventario(sesion):
    if sesion is None:
        print("Acceso rechazado.")
        return False

    productos = cargar_inventario()
    for producto in productos:
        print(producto["id"], producto["nombre"], producto["cantidad"])
    return True


def modificar_cantidad(sesion, identificador, entrada):
    if sesion is None or sesion.get("rol") != "admin":
        registrar_evento(
            sesion["usuario"] if sesion else "anonimo",
            "modificar",
            "rechazado",
            producto=identificador,
            motivo="sin permisos"
        )
        print("Acceso rechazado.")
        return False

    try:
        cantidad = int(entrada)
    except (TypeError, ValueError):
        print("La cantidad debe ser un número entero.")
        return False

    if cantidad < 0 or cantidad > 1000:
        print("La cantidad debe estar entre 0 y 1000.")
        return False

    productos = cargar_inventario()

    for producto in productos:
        if producto["id"] == identificador:
            anterior = producto["cantidad"]
            producto["cantidad"] = cantidad
            guardar_inventario(productos)
            registrar_evento(
                sesion["usuario"],
                "modificar",
                "exitoso",
                producto=identificador,
                anterior=anterior,
                nueva=cantidad
            )
            print("Cantidad actualizada.")
            return True

    registrar_evento(
        sesion["usuario"],
        "modificar",
        "rechazado",
        producto=identificador,
        motivo="producto inexistente"
    )
    print("Producto inexistente.")
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
