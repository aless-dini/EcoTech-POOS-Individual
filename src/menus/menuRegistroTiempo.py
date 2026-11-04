from dominio.registroTiempo import RegistroTiempo
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from entradas import pedir_dato
from menus.menuEmpleado import pedir_entero
from persistencia.errores import registro as registro_errores
from servicios import registros
from servicios.mi_cuenta import mis_registros
from servicios.permisos import es_administrador, exigir_admin, exigir_sesion

# Las funciones de administración comprueban el permiso antes de usar el DAO,
# aunque el menú ya oculte la opción (el PermissionError lo muestra el menú principal).

def pedir_empleado_segun_rol(usuario_actual):
    # El admin elige el empleado; el empleado siempre usa el suyo, tomado de la sesión.
    if es_administrador(usuario_actual):
        idEmpleado = pedir_entero("\nIngrese el id del empleado: ")
    else:
        idEmpleado = usuario_actual["empleado_id"]
    empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
    if empleado is None:
        print("\nNo existe un empleado con ese id")
    return empleado

def pedir_fecha(mensaje):
    return pedir_dato(mensaje, RegistroTiempo.validar_fecha_registro)

def pedir_horas(mensaje):
    return pedir_dato(mensaje, RegistroTiempo.validar_horas)

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
    exigir_sesion(usuario_actual)
    empleado = pedir_empleado_segun_rol(usuario_actual)
    if empleado is None:
        return

    idProyecto = pedir_entero("Ingrese el id del proyecto: ")
    proyecto = ProyectoDAO.buscar_por_id(idProyecto)
    if proyecto is None:
        print("\nNo existe un proyecto con ese id")
        return
    if not registros.esta_asignado(empleado.id, proyecto.id):
        print("\nEl empleado no está asignado a ese proyecto, primero asígnelo en el menú de proyectos")
        return

    fecha = pedir_fecha("Fecha (DD-MM-AAAA): ")
    horas = pedir_horas("Horas trabajadas: ")

    registro = RegistroTiempo(fecha, horas, empleado.id, proyecto.id)
    try:
        guardado = registros.registrar(registro)
    except ValueError as error:
        print(f"\n{error}")
        return
    if guardado is not None:
        print(f"\nSe registraron {horas:g} horas de {empleado.nombre} en '{proyecto.nombre}'")
    else:
        print("\nNo fue posible registrar las horas")

def editar_registro(usuario_actual):
    exigir_admin(usuario_actual)
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

    try:
        actualizado = registros.actualizar(registro)
    except ValueError as error:
        print(f"\n{error}")
        return
    if actualizado:
        print("\nRegistro actualizado correctamente")
    else:
        print("\nNo fue posible actualizar el registro")

def eliminar_registro(usuario_actual):
    exigir_admin(usuario_actual)
    idRegistro = pedir_entero("Ingrese el id del registro que desea eliminar: ")
    if RegistroTiempoDAO.eliminar(idRegistro):
        print("\nRegistro eliminado correctamente")
    else:
        print("\nNo existe un registro con ese id")

def listar_registros(usuario_actual):
    exigir_admin(usuario_actual)
    mostrar_registros(RegistroTiempoDAO.listar_todos())

def listar_registros_empleado(usuario_actual):
    exigir_admin(usuario_actual)
    empleado = pedir_empleado_segun_rol(usuario_actual)
    if empleado is None:
        return
    mostrar_registros(RegistroTiempoDAO.listar_por_empleado(empleado.id))

def ver_mis_registros(usuario_actual):
    try:
        propios = mis_registros(usuario_actual)
    except PermissionError as error:
        print(f"\n{error}")
        return
    mostrar_registros(propios)

def listar_registros_proyecto(usuario_actual):
    exigir_admin(usuario_actual)
    idProyecto = pedir_entero("Ingrese el id del proyecto: ")
    if ProyectoDAO.buscar_por_id(idProyecto) is None:
        print("\nNo existe un proyecto con ese id")
        return
    mostrar_registros(RegistroTiempoDAO.listar_por_proyecto(idProyecto))

def exportar_informe_empleado(usuario_actual):
    exigir_sesion(usuario_actual)
    empleado = pedir_empleado_segun_rol(usuario_actual)
    if empleado is None:
        return

    registros = RegistroTiempoDAO.listar_por_empleado(empleado.id)
    if not registros:
        print("\nEl empleado no tiene horas registradas")
        return

    ruta = f"informe_{empleado.id}.txt"
    try:
        # exportar_informe agrega al final: se vacía el archivo para no repetir un informe anterior.
        open(ruta, "w", encoding="utf-8").close()
        for registro in registros:
            registro.exportar_informe(ruta)
    except OSError:
        registro_errores.error("No se pudo escribir %s", ruta, exc_info=True)
        print(f"\nNo fue posible escribir el informe en {ruta}: revise que el archivo no esté abierto "
              "y que tenga permisos en la carpeta.")
        return
    print(f"\nInforme de {empleado.nombre} exportado en {ruta} ({len(registros)} registros)")
