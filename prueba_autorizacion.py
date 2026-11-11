import app

antes = app.cargar_inventario()
print("Cantidad original:", antes[0]["cantidad"])

sesion_user = app.autenticar("user", "UserDemo2700!")
print("Sesión user:", sesion_user)

resultado = app.modificar_cantidad(sesion_user, "P001", "99")
print("Resultado user:", resultado)

resultado = app.modificar_cantidad(None, "P001", "99")
print("Resultado sin sesión:", resultado)

resultado = app.consultar_inventario(None)
print("Consulta sin sesión:", resultado)

despues = app.cargar_inventario()
print("Cantidad final:", despues[0]["cantidad"])