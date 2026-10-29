from dominio.proyecto import Proyecto
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from entradas import pedir_dato, pedir_opcional
from menus.menuEmpleado import pedir_entero, mostrar_lista
from servicios.registros import esta_asignado, validar_inicio_proyecto

def pedir_proyecto_existente(mensaje):
    idProyecto = pedir_entero(mensaje)
    proyecto = ProyectoDAO.buscar_por_id(idProyecto)
    if proyecto is None:
        print("\nNo existe un proyecto con ese id")
    return proyecto

def crear_proyecto():
    nombre = pedir_dato("\nNombre del proyecto: ", Proyecto.validar_nombre)
    descripcion = pedir_dato("Descripción: ", Proyecto.validar_descripcion)
    fechaInicio = pedir_dato("Fecha de inicio (DD-MM-AAAA): ", Proyecto.validar_fecha_inicio)

    proyecto = Proyecto(nombre, descripcion, fechaInicio)
    if ProyectoDAO.insertar(proyecto) is not None:
        print(f"\nProyecto '{proyecto.nombre}' creado correctamente con id {proyecto.id}")
    else:
        print("\nNo fue posible crear el proyecto")

def editar_proyecto():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto que desea editar: ")
    if proyecto is None:
        return

    print("\nDatos actuales:")
    print(f"Id: {proyecto.id} | Nombre: {proyecto.nombre} | Inicio: {proyecto.fechaInicio}")
    print(f"Descripción: {proyecto.descripcion}")

    nombre = pedir_opcional(f"\nNuevo nombre (Enter para mantener '{proyecto.nombre}'): ", Proyecto.validar_nombre)
    if nombre:
        proyecto.nombre = nombre

    descripcion = pedir_opcional("Nueva descripción (Enter para mantener la actual): ", Proyecto.validar_descripcion)
    if descripcion:
        proyecto.descripcion = descripcion

    if input("¿Cambiar la fecha de inicio? (s/n): ").strip().lower() == "s":
        proyecto.fechaInicio = pedir_dato(
            "Nueva fecha de inicio (DD-MM-AAAA): ",
            lambda valor: validar_inicio_proyecto(proyecto.id, Proyecto.validar_fecha_inicio(valor)),
        )

    if ProyectoDAO.actualizar(proyecto):
        print("\nProyecto actualizado correctamente")
    else:
        print("\nNo fue posible actualizar el proyecto")

def eliminar_proyecto():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto que desea eliminar: ")
    if proyecto is None:
        return

    if RegistroTiempoDAO.listar_por_proyecto(proyecto.id):
        print("\nNo se puede eliminar un proyecto que tiene horas registradas")
        return

    for empleado in EmpleadoDAO.listar_por_proyecto(proyecto.id):
        ProyectoDAO.quitar_empleado(proyecto.id, empleado.id)

    if ProyectoDAO.eliminar(proyecto.id):
        print("\nProyecto eliminado correctamente")
    else:
        print("\nNo fue posible eliminar el proyecto")

def listar_proyectos():
    proyectos = ProyectoDAO.listar_todos()
    if not proyectos:
        print("\nNo hay proyectos registrados.")
        return
    for proyecto in proyectos:
        print(f"\nId {proyecto.id}, Nombre {proyecto.nombre}, Inicio {proyecto.fechaInicio}")

def buscar_proyecto_por_id():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto que desea buscar: ")
    if proyecto is None:
        return

    empleados = EmpleadoDAO.listar_por_proyecto(proyecto.id)
    horas = sum(float(r.horas) for r in RegistroTiempoDAO.listar_por_proyecto(proyecto.id))
    print(f"\nProyecto {proyecto.nombre} (ID {proyecto.id})")
    print(f"Descripción: {proyecto.descripcion}")
    print(f"Inicio: {proyecto.fechaInicio} | Empleados: {len(empleados)} | Horas registradas: {horas:g}")

def asignar_empleado_proyecto():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto: ")
    if proyecto is None:
        return

    idEmpleado = pedir_entero("Ingrese el id del empleado que desea asignar: ")
    empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
    if empleado is None:
        print("\nNo existe un empleado con ese id")
        return
    if esta_asignado(empleado.id, proyecto.id):
        print("\nEl empleado ya está asignado a este proyecto")
        return

    if ProyectoDAO.asignar_empleado(proyecto.id, empleado.id):
        print(f"\nEmpleado {empleado.nombre} asignado al proyecto '{proyecto.nombre}'")
    else:
        print("\nNo fue posible asignar el empleado al proyecto")

def quitar_empleado_proyecto():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto: ")
    if proyecto is None:
        return

    idEmpleado = pedir_entero("Ingrese el id del empleado que desea quitar: ")
    if ProyectoDAO.quitar_empleado(proyecto.id, idEmpleado):
        print(f"\nEmpleado quitado del proyecto '{proyecto.nombre}'")
    else:
        print("\nEse empleado no está asignado a este proyecto")

def listar_empleados_proyecto():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto: ")
    if proyecto is None:
        return

    mostrar_lista(EmpleadoDAO.listar_por_proyecto(proyecto.id))
