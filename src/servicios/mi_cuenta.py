from dominio.empleado import Empleado
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from servicios.permisos import exigir_sesion


def mi_ficha(sesion):
    # El ID sale de la sesión, nunca de un dato escrito por el usuario.
    exigir_sesion(sesion)
    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("Empleado no encontrado.")
    return empleado


def mis_registros(sesion):
    exigir_sesion(sesion)
    return RegistroTiempoDAO.listar_por_empleado(sesion["empleado_id"])


def mis_proyectos(sesion):
    # Solo los proyectos a los que está asignado el empleado de la sesión.
    exigir_sesion(sesion)
    return ProyectoDAO.listar_por_empleado(sesion["empleado_id"])


def mi_departamento(sesion):
    # None si el empleado no pertenece a ningún departamento.
    empleado = mi_ficha(sesion)
    if empleado.id_departamento is None:
        return None
    return DepartamentoDAO.buscar_por_id(empleado.id_departamento)


def actualizar_mis_datos(sesion, nombre, correo):
    # Solo nombre y correo: el rol, el ID y el departamento no se tocan aquí.
    exigir_sesion(sesion)
    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)

    empleado = mi_ficha(sesion)
    existente = EmpleadoDAO.buscar_por_correo(correo)
    if existente is not None and existente.id != empleado.id:
        raise ValueError("Ese correo ya está registrado por otro empleado.")

    empleado.nombre, empleado.correo = nombre, correo
    return EmpleadoDAO.actualizar(empleado)
