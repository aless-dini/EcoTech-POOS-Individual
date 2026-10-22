import sys
from getpass import getpass
from dominio.usuario import Usuario
from entradas import pedir_dato
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import registrar_usuario, autenticar, cambiar_clave
from menus.menuEmpleado import a_entero_positivo

def pedir_contraseña(mensaje):
    # getpass oculta lo escrito, pero no funciona en todas las consolas.
    if sys.stdin.isatty():
        return getpass(mensaje)
    return input(mensaje)

def validar_id(valor):
    numero = a_entero_positivo(valor)
    if numero is None:
        raise ValueError("El ID debe ser un número entero positivo.")
    return numero

def solicitar_registro():
    try:
        id_empleado = pedir_dato("\nID del empleado: ", validar_id)
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato(f"Contraseña (mínimo {Usuario.MIN_CLAVE} caracteres): ",
                           Usuario.validar_clave, pedir_contraseña)
        if clave != pedir_contraseña("Repita la contraseña: "):
            print("\nLas contraseñas no coinciden. Vuelva al registro.")
            return None
        rol = pedir_dato(f"Rol ({' / '.join(Usuario.ROLES)}): ", Usuario.validar_rol)
        usuario_id = registrar_usuario(id_empleado, nombre, clave, rol)
    except (TypeError, ValueError) as error:
        print(f"\n{error}")
        return None

    print(f"\nCuenta creada correctamente. ID: {usuario_id}")
    return usuario_id

def solicitar_login():
    nombre = input("\nUsuario: ")
    clave = pedir_contraseña("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("\nUsuario o contraseña incorrectos.")
        return None
    if usuario is None:
        print("\nUsuario o contraseña incorrectos.")
    else:
        print(f"\nSesión iniciada correctamente. Bienvenido/a, {usuario['nombre_usuario']}")
    return usuario

def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("\nInicie sesión para ver el perfil.")
        return
    print(f"\nUsuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado: {usuario_actual['id_empleado']}")
    print(f"Rol: {usuario_actual['rol']}")

def cambiar_contraseña(usuario_actual):
    actual = pedir_contraseña("\nContraseña actual: ")
    nueva = pedir_dato(f"Nueva contraseña (mínimo {Usuario.MIN_CLAVE} caracteres): ",
                       Usuario.validar_clave, pedir_contraseña)
    if nueva != pedir_contraseña("Repita la nueva contraseña: "):
        print("\nLas contraseñas no coinciden")
        return
    try:
        cambiada = cambiar_clave(usuario_actual["id"], actual, nueva)
    except (TypeError, ValueError) as error:
        print(f"\n{error}")
        return
    if cambiada:
        print("\nContraseña cambiada correctamente")
    else:
        print("\nNo fue posible cambiar la contraseña")

def pedir_usuario_por_id(mensaje):
    usuario = UsuarioDAO.buscar_por_id(pedir_dato(mensaje, validar_id))
    if usuario is None:
        print("\nNo existe un usuario con ese id")
    return usuario

def mostrar_usuario(usuario):
    print(f"\nId {usuario.id}, Usuario {usuario.nombre_usuario}, Rol {usuario.rol}, Empleado {usuario.id_empleado}")

def editar_usuario():
    usuario = pedir_usuario_por_id("\nId del usuario que desea editar: ")
    if usuario is None:
        return

    mostrar_usuario(usuario)
    usuario.rol = pedir_dato(f"Nuevo rol ({' / '.join(Usuario.ROLES)}): ", Usuario.validar_rol)

    if UsuarioDAO.actualizar(usuario):
        print("\nUsuario actualizado correctamente")
    else:
        print("\nNo fue posible actualizar el usuario")

def eliminar_usuario(usuario_actual):
    usuario = pedir_usuario_por_id("\nId del usuario que desea eliminar: ")
    if usuario is None:
        return
    if usuario.id == usuario_actual["id"]:
        print("\nNo puede eliminar la cuenta con la que inició sesión")
        return

    if input(f"¿Seguro que desea eliminar a '{usuario.nombre_usuario}'? (s/n): ").strip().lower() != "s":
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
        mostrar_usuario(usuario)

def buscar_usuario_por_id():
    usuario = pedir_usuario_por_id("\nId del usuario: ")
    if usuario is not None:
        mostrar_usuario(usuario)
