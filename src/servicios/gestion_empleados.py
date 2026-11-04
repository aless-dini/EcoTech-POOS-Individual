from persistencia.empleado_dao import EmpleadoDAO
from servicios.permisos import exigir_admin


# Consultas sobre otros empleados: solo el administrador.
# El empleado consulta sus propios datos desde servicios/mi_cuenta.py.

def listar_todos(sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.listar_todos()


def listar_por_departamento(sesion, id_departamento):
    exigir_admin(sesion)
    return EmpleadoDAO.listar_por_departamento(id_departamento)


def listar_por_proyecto(sesion, id_proyecto):
    exigir_admin(sesion)
    return EmpleadoDAO.listar_por_proyecto(id_proyecto)


def buscar_por_id(sesion, id_empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.buscar_por_id(id_empleado)


def buscar_por_nombre(sesion, nombre):
    exigir_admin(sesion)
    return EmpleadoDAO.buscar_por_nombre(nombre)
