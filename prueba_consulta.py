import app

admin = app.autenticar("admin", "AdminDemo2700!")
user = app.autenticar("user", "UserDemo2700!")

print("Consulta de admin:")
app.consultar_inventario(admin)

print("Consulta de user:")
app.consultar_inventario(user)

print("Cambio de P001 a 20:")
print(app.modificar_cantidad(admin, "P001", "20"))

print("Intento de modificar P999:")
print(app.modificar_cantidad(admin, "P999", "50"))

print("Inventario final:")
app.consultar_inventario(admin)