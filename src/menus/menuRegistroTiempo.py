from dominio.registroTiempo import RegistroTiempo
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from menus.menuEmpleado import pedir_entero, pedir_fecha
from servicios.autenticacion import es_administrador

def pedir_empleado_segun_rol(usuario_actual):
    # El administrador elige al empleado. Un empleado común solo puede
    # trabajar con sus propias horas, por eso se usa el id de su sesión.
    if es_administrador(usuario_actual):
        idEmpleado = pedir_entero("\nIngrese el id del empleado: ")
    else:
        idEmpleado = usuario_actual["id_empleado"]
    empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
    if empleado is None:
        print("\nNo existe un empleado con ese id")
    return empleado

def pedir_horas(mensaje):
    while True:
        valor = input(mensaje).strip().replace(",", ".")
        try:
            horas = float(valor)
        except ValueError:
            print("Debe ingresar un número (por ejemplo 8 o 7,5), intente de nuevo.")
            continue
        if not 0 < horas <= 24:
            print("Las horas deben ser mayores que 0 y como máximo 24, intente de nuevo.")
            continue
        return horas

def describir(registro):
    empleado = EmpleadoDAO.buscar_por_id(registro.id_empleado)
    proyecto = ProyectoDAO.buscar_por_id(registro.id_proyecto)
    nombre_empleado = empleado.nombre if empleado else f"id {registro.id_empleado}"
    nombre_proyecto = proyecto.nombre if proyecto else f"id {registro.id_proyecto}"
    return (f"Id {registro.id} | {registro.mostrar_registro()} horas | "
            f"Empleado: {nombre_empleado} | Proyecto: {nombre_proyecto}")

def mostrar_registros(registros):
    if not registros:
        print("\nNo se encontraron registros.")
        return
    for registro in registros:
        print(describir(registro))
    total = sum(float(r.horas) for r in registros)
    print(f"\nTotal: {total:g} horas")

def registrar_horas(usuario_actual):
    empleado = pedir_empleado_segun_rol(usuario_actual)
    if empleado is None:
        return

    idProyecto = pedir_entero("Ingrese el id del proyecto: ")
    proyecto = ProyectoDAO.buscar_por_id(idProyecto)
    if proyecto is None:
        print("\nNo existe un proyecto con ese id")
        return
    if not any(e.id == empleado.id for e in EmpleadoDAO.listar_por_proyecto(proyecto.id)):
        print("\nEl empleado no está asignado a ese proyecto, primero asígnelo en el menú de proyectos")
        return

    fecha = pedir_fecha("Fecha (DD-MM-AAAA): ")
    horas = pedir_horas("Horas trabajadas: ")

    registro = RegistroTiempo(fecha, horas, empleado.id, proyecto.id)
    if RegistroTiempoDAO.insertar(registro) is not None:
        print(f"\nSe registraron {horas:g} horas de {empleado.nombre} en '{proyecto.nombre}'")
    else:
        print("\nNo fue posible registrar las horas")

def editar_registro():
    idRegistro = pedir_entero("Ingrese el id del registro que desea editar: ")
    registro = RegistroTiempoDAO.buscar_por_id(idRegistro)
    if registro is None:
        print("\nNo existe un registro con ese id")
        return

    print("\nDatos actuales:")
    print(describir(registro))

    if input("\n¿Cambiar la fecha? (s/n): ").strip().lower() == "s":
        registro.fecha = pedir_fecha("Nueva fecha (DD-MM-AAAA): ")
    if input("¿Cambiar las horas? (s/n): ").strip().lower() == "s":
        registro.horas = pedir_horas("Nuevas horas trabajadas: ")

    if RegistroTiempoDAO.actualizar(registro):
        print("\nRegistro actualizado correctamente")
    else:
        print("\nNo fue posible actualizar el registro")

def eliminar_registro():
    idRegistro = pedir_entero("Ingrese el id del registro que desea eliminar: ")
    if RegistroTiempoDAO.eliminar(idRegistro):
        print("\nRegistro eliminado correctamente")
    else:
        print("\nNo existe un registro con ese id")

def listar_registros():
    mostrar_registros(RegistroTiempoDAO.listar_todos())

def listar_registros_empleado(usuario_actual):
    empleado = pedir_empleado_segun_rol(usuario_actual)
    if empleado is None:
        return
    mostrar_registros(RegistroTiempoDAO.listar_por_empleado(empleado.id))

def listar_registros_proyecto():
    idProyecto = pedir_entero("Ingrese el id del proyecto: ")
    if ProyectoDAO.buscar_por_id(idProyecto) is None:
        print("\nNo existe un proyecto con ese id")
        return
    mostrar_registros(RegistroTiempoDAO.listar_por_proyecto(idProyecto))

def exportar_informe_empleado(usuario_actual):
    empleado = pedir_empleado_segun_rol(usuario_actual)
    if empleado is None:
        return

    registros = RegistroTiempoDAO.listar_por_empleado(empleado.id)
    if not registros:
        print("\nEl empleado no tiene horas registradas")
        return

    ruta = f"informe_{empleado.id}.txt"
    try:
        for registro in registros:
            registro.exportar_informe(ruta)
    except OSError as e:
        print(f"\nNo fue posible escribir el informe: {e}")
        return
    print(f"\nInforme de {empleado.nombre} exportado en {ruta} ({len(registros)} registros)")
