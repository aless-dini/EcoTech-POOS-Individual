from datetime import date
from dominio.registroTiempo import RegistroTiempo
from dominio.validaciones import a_fecha
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registroTiempo_dao import RegistroTiempoDAO


def esta_asignado(id_empleado, id_proyecto):
    return any(e.id == id_empleado for e in EmpleadoDAO.listar_por_proyecto(id_proyecto))


def horas_del_dia(id_empleado, fecha, excepto=None):
    return sum(r.horas for r in RegistroTiempoDAO.listar_por_empleado(id_empleado)
               if r.fecha == fecha and r.id != excepto)


def validar_registro(registro: RegistroTiempo):
    proyecto = ProyectoDAO.buscar_por_id(registro.id_proyecto)
    if proyecto is None:
        raise ValueError("No existe un proyecto con ese id.")
    if not esta_asignado(registro.id_empleado, proyecto.id):
        raise ValueError("El empleado no está asignado a ese proyecto, primero asígnelo en el menú de proyectos.")

    fecha = a_fecha(registro.fecha)
    if fecha > date.today():
        raise ValueError("No se pueden registrar horas en una fecha futura.")
    if fecha < a_fecha(proyecto.fechaInicio):
        raise ValueError(f"La fecha no puede ser anterior al inicio del proyecto ({proyecto.fechaInicio}).")

    ya_registradas = horas_del_dia(registro.id_empleado, registro.fecha, excepto=registro.id)
    if round(ya_registradas + registro.horas, 2) > RegistroTiempo.MAX_HORAS:
        disponibles = RegistroTiempo.MAX_HORAS - ya_registradas
        raise ValueError(f"El empleado ya tiene {ya_registradas:g} horas el {registro.fecha}; "
                         f"solo puede registrar {disponibles:g} más ese día.")


def validar_inicio_proyecto(id_proyecto, fecha_inicio):
    # Al mover el inicio de un proyecto no pueden quedar horas registradas antes de él.
    fechas = [a_fecha(r.fecha) for r in RegistroTiempoDAO.listar_por_proyecto(id_proyecto)]
    if fechas and min(fechas) < a_fecha(fecha_inicio):
        raise ValueError(f"El proyecto tiene horas registradas desde el {min(fechas):%d-%m-%Y}; "
                         "la fecha de inicio no puede ser posterior.")
    return fecha_inicio


def registrar(registro: RegistroTiempo):
    validar_registro(registro)
    return RegistroTiempoDAO.insertar(registro)


def actualizar(registro: RegistroTiempo):
    validar_registro(registro)
    return RegistroTiempoDAO.actualizar(registro)
