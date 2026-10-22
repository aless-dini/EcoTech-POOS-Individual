import bcrypt
from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO
from persistencia.empleado_dao import EmpleadoDAO

MAX_BYTES_BCRYPT = 72


def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")


def verificar_clave(clave, password_hash):
    if not isinstance(clave, str):
        return False
    datos = clave.encode("utf-8")
    if not 0 < len(datos) <= MAX_BYTES_BCRYPT:
        return False
    return bcrypt.checkpw(datos, password_hash.encode("utf-8"))


def registrar_usuario(id_empleado, nombre, clave, rol="empleado"):
    nombre = Usuario.normalizar_usuario(nombre)
    if EmpleadoDAO.buscar_por_id(id_empleado) is None:
        raise ValueError("No existe un empleado con ese ID.")
    if UsuarioDAO.buscar_por_empleado(id_empleado) is not None:
        raise ValueError("Ese empleado ya tiene una cuenta.")
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        raise ValueError("No se pudo crear esa cuenta.")

    hash_guardado = crear_hash(clave)
    usuario = Usuario(nombre, hash_guardado, id_empleado, rol)

    usuario = UsuarioDAO.insertar(usuario)
    if usuario is None:
        raise ValueError("No fue posible guardar la cuenta.")
    return usuario.id


def autenticar(nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    cuenta = UsuarioDAO.buscar_por_nombre(nombre)
    if cuenta is None or not verificar_clave(clave, cuenta.password_hash):
        return None
    return {"id": cuenta.id, "id_empleado": cuenta.id_empleado,
            "nombre_usuario": cuenta.nombre_usuario, "rol": cuenta.rol}


def es_administrador(usuario_actual):
    return usuario_actual is not None and usuario_actual["rol"] == "administrador"


def cambiar_clave(id_usuario, clave_actual, clave_nueva):
    cuenta = UsuarioDAO.buscar_por_id(id_usuario)
    if cuenta is None or not verificar_clave(clave_actual, cuenta.password_hash):
        raise ValueError("Contraseña actual incorrecta.")
    cuenta.password_hash = crear_hash(clave_nueva)
    return UsuarioDAO.actualizar(cuenta)
