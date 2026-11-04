from dominio.usuario import Usuario


def exigir_sesion(sesion):
    if not isinstance(sesion, dict):
        raise PermissionError("Inicie sesión.")
    if sesion.get("rol") not in Usuario.ROLES:
        raise PermissionError("Acceso no permitido.")
    empleado_id = sesion.get("empleado_id")
    if type(empleado_id) is not int or empleado_id <= 0:
        raise PermissionError("Sesión inválida.")


def exigir_admin(sesion):
    exigir_sesion(sesion)
    if sesion["rol"] != "admin":
        raise PermissionError("Acción solo para administrador.")


def es_administrador(sesion):
    return isinstance(sesion, dict) and sesion.get("rol") == "admin"
