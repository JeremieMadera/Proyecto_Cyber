import app

sesion = app.autenticar("admin", "AdminDemo2700!")
casos = ["-1", "1001", "abc", "2.5", "", "0", "1000"]

for entrada in casos:
    app.modificar_cantidad(sesion, "P001", "10")
    antes = app.cargar_inventario()[0]["cantidad"]

    resultado = app.modificar_cantidad(sesion, "P001", entrada)
    despues = app.cargar_inventario()[0]["cantidad"]

    print(
        f"Entrada: {entrada!r} | "
        f"Resultado: {'ACEPTADA' if resultado else 'RECHAZADA'} | "
        f"Cantidad: {antes} -> {despues}"
    )

# Restaurar P001 a 10
app.modificar_cantidad(sesion, "P001", "10")
print("Cantidad final:", app.cargar_inventario()[0]["cantidad"])