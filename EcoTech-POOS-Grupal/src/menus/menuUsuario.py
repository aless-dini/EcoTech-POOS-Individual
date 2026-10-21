import sys
from getpass import getpass
from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO
from persistencia.empleado_dao import EmpleadoDAO
from menus.menuEmpleado import pedir_texto, a_entero_positivo

ROLES = ("administrador", "empleado")

def pedir_contraseña(mensaje):
    if sys.stdin.isatty():
        return getpass(mensaje)
    return input(mensaje)

def gestionar_usuarios():
    print("\n1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Cambiar contraseña")
    print("4. Editar usuario")
    print("5. Eliminar usuario")
    print("6. Listar usuarios")
    print("7. Volver")

def pedir_rol(mensaje):
    while True:
        rol = input(mensaje).strip().lower()
        if rol in ROLES:
            return rol
        print(f"El rol debe ser uno de estos: {', '.join(ROLES)}. Intente de nuevo.")

def pedir_empleado_opcional(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor == "":
            return None
        id_empleado = a_entero_positivo(valor)
        if id_empleado is None:
            print("El id del empleado debe ser un número entero positivo, intente de nuevo.")
            continue
        if EmpleadoDAO.buscar_por_id(id_empleado) is None:
            print("No existe un empleado con ese id, intente de nuevo.")
            continue
        return id_empleado

def crear_usuario_con_contraseña(nombre, rol, id_empleado, id=None):
    while True:
        contraseña = pedir_contraseña("Contraseña (mínimo 8 caracteres): ")
        try:
            return Usuario(nombre, contraseña, rol, id_empleado, id)
        except ValueError as e:
            print(f"{e}, intente de nuevo.")

def pedir_usuario_existente(mensaje):
    nombre = pedir_texto(mensaje)
    usuario = UsuarioDAO.buscar_por_nombre(nombre)
    if usuario is None:
        print("\nNo existe un usuario con ese nombre")
    return usuario

def registrar_usuario():
    nombre = pedir_texto("\nNombre de usuario: ")
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        print("\nYa existe un usuario con ese nombre")
        return

    usuario = crear_usuario_con_contraseña(nombre, None, None)
    usuario.rol = pedir_rol(f"Rol ({' / '.join(ROLES)}): ")
    usuario.id_empleado = pedir_empleado_opcional("Id del empleado asociado (Enter si no es empleado): ")

    if not usuario.registrar():
        print("\nFaltan datos para registrar el usuario")
        return

    if UsuarioDAO.insertar(usuario) is not None:
        print(f"\nUsuario '{usuario.nombre}' registrado correctamente con id {usuario.id}")
    else:
        print("\nNo fue posible registrar el usuario")

def iniciar_sesion():
    usuario = pedir_usuario_existente("\nNombre de usuario: ")
    if usuario is None:
        return

    contraseña = pedir_contraseña("Contraseña: ")
    if usuario.iniciar_sesion(contraseña):
        print(f"\nBienvenido/a, {usuario.nombre} (rol: {usuario.rol})")
    else:
        print("\nContraseña incorrecta")

def cambiar_contraseña():
    usuario = pedir_usuario_existente("\nNombre de usuario: ")
    if usuario is None:
        return

    if not usuario.iniciar_sesion(pedir_contraseña("Contraseña actual: ")):
        print("\nContraseña incorrecta")
        return

    nuevo = crear_usuario_con_contraseña(usuario.nombre, usuario.rol, usuario.id_empleado, usuario.id)
    if UsuarioDAO.actualizar(nuevo):
        print("\nContraseña cambiada correctamente")
    else:
        print("\nNo fue posible cambiar la contraseña")

def editar_usuario():
    usuario = pedir_usuario_existente("\nNombre del usuario que desea editar: ")
    if usuario is None:
        return

    empleado = "Ninguno" if usuario.id_empleado is None else usuario.id_empleado
    print(f"\nDatos actuales: Rol: {usuario.rol} | Empleado asociado: {empleado}")

    if input("\n¿Cambiar el rol? (s/n): ").strip().lower() == "s":
        usuario.rol = pedir_rol(f"Nuevo rol ({' / '.join(ROLES)}): ")
    if input("¿Cambiar el empleado asociado? (s/n): ").strip().lower() == "s":
        usuario.id_empleado = pedir_empleado_opcional("Id del empleado (Enter para dejarlo sin empleado): ")

    if UsuarioDAO.actualizar(usuario):
        print("\nUsuario actualizado correctamente")
    else:
        print("\nNo fue posible actualizar el usuario")

def eliminar_usuario():
    usuario = pedir_usuario_existente("\nNombre del usuario que desea eliminar: ")
    if usuario is None:
        return

    if input(f"¿Seguro que desea eliminar a '{usuario.nombre}'? (s/n): ").strip().lower() != "s":
        print("\nNo se eliminó el usuario")
        return

    if UsuarioDAO.eliminar(usuario.id):
        print("\nUsuario eliminado correctamente")
    else:
        print("\nNo fue posible eliminar el usuario")

def listar_usuarios():
    usuarios = UsuarioDAO.listar_todos()
    if not usuarios:
        print("\nNo hay usuarios registrados.")
        return
    for usuario in usuarios:
        empleado = "Ninguno" if usuario.id_empleado is None else usuario.id_empleado
        print(f"\nId {usuario.id}, Nombre {usuario.nombre}, Rol {usuario.rol}, Empleado {empleado}")
