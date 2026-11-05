from menus.menuEmpleado import (
    registrar_empleado, actualizar_empleado, eliminar_empleado,
    listar_empleados, listar_empleados_por_departamento,
    buscar_empleado_por_id, buscar_empleado_por_nombre,
    mostrar_mi_ficha, editar_mis_datos,
)
from menus.menuDepartamento import (
    crear_departamento, eliminar_departamento,
    agregar_empleado_departamento, quitar_empleado_departamento,
    listar_empleados_departamento, ver_cantidad_empleados, editar_departamento,
    mostrar_mi_departamento,
)
from menus.menuProyecto import (
    crear_proyecto, editar_proyecto, eliminar_proyecto,
    listar_proyectos, buscar_proyecto_por_id, asignar_empleado_proyecto,
    quitar_empleado_proyecto, listar_empleados_proyecto, mostrar_mis_proyectos,
)
from menus.menuRegistroTiempo import (
    registrar_horas, editar_registro, eliminar_registro,
    listar_registros, listar_registros_empleado, listar_registros_proyecto,
    exportar_informe_empleado, ver_mis_registros,
)
from menus.menuUsuario import (
    solicitar_registro, cambiar_contraseña, editar_usuario, eliminar_usuario,
    listar_usuarios, buscar_usuario_por_id, mostrar_perfil,
)
from menus.menuIndicadores import consultar_valor_actualizado, ver_historial_guardado
from persistencia.errores import ErrorBaseDatos
from servicios.permisos import es_administrador

ADMIN = "admin"
EMPLEADO = "empleado"
TODOS = "todos"

def crear_submenus():
    # Cada acción recibe la sesión: el menú decide qué mostrar y la función vuelve a comprobar el permiso.
    return {
        "1": ("Empleados", [
            ("Registrar empleado", registrar_empleado, ADMIN),
            ("Actualizar empleado", actualizar_empleado, ADMIN),
            ("Eliminar empleado", eliminar_empleado, ADMIN),
            ("Listar empleados", listar_empleados, ADMIN),
            ("Listar empleados por departamento", listar_empleados_por_departamento, ADMIN),
            ("Buscar empleado por id", buscar_empleado_por_id, ADMIN),
            ("Buscar empleado por nombre", buscar_empleado_por_nombre, ADMIN),
            ("Mi ficha", mostrar_mi_ficha, EMPLEADO),
            ("Actualizar mis datos", editar_mis_datos, EMPLEADO),
        ]),
        "2": ("Departamentos", [
            ("Crear departamento", crear_departamento, ADMIN),
            ("Editar departamento", editar_departamento, ADMIN),
            ("Eliminar departamento", eliminar_departamento, ADMIN),
            ("Agregar empleado al departamento", agregar_empleado_departamento, ADMIN),
            ("Quitar empleado del departamento", quitar_empleado_departamento, ADMIN),
            ("Listar empleados del departamento", listar_empleados_departamento, ADMIN),
            ("Ver cantidad de empleados", ver_cantidad_empleados, ADMIN),
            ("Mi departamento", mostrar_mi_departamento, EMPLEADO),
        ]),
        "3": ("Proyectos", [
            ("Crear proyecto", crear_proyecto, ADMIN),
            ("Editar proyecto", editar_proyecto, ADMIN),
            ("Eliminar proyecto", eliminar_proyecto, ADMIN),
            ("Asignar empleado al proyecto", asignar_empleado_proyecto, ADMIN),
            ("Quitar empleado del proyecto", quitar_empleado_proyecto, ADMIN),
            ("Listar proyectos", listar_proyectos, ADMIN),
            ("Buscar proyecto por id", buscar_proyecto_por_id, ADMIN),
            ("Listar empleados del proyecto", listar_empleados_proyecto, ADMIN),
            ("Mis proyectos", mostrar_mis_proyectos, EMPLEADO),
        ]),
        "4": ("Registros de tiempo", [
            ("Registrar horas", registrar_horas, ADMIN),
            ("Registrar mis horas", registrar_horas, EMPLEADO),
            ("Editar registro", editar_registro, ADMIN),
            ("Eliminar registro", eliminar_registro, ADMIN),
            ("Listar todos los registros", listar_registros, ADMIN),
            ("Listar registros de un empleado", listar_registros_empleado, ADMIN),
            ("Ver mis registros", ver_mis_registros, EMPLEADO),
            ("Listar registros de un proyecto", listar_registros_proyecto, ADMIN),
            ("Exportar informe de un empleado", exportar_informe_empleado, ADMIN),
            ("Exportar mi informe", exportar_informe_empleado, EMPLEADO),
        ]),
        "5": ("Usuarios", [
            ("Registrar usuario", solicitar_registro, ADMIN),
            ("Cambiar mi contraseña", cambiar_contraseña, TODOS),
            ("Editar rol de un usuario", editar_usuario, ADMIN),
            ("Eliminar usuario", eliminar_usuario, ADMIN),
            ("Listar usuarios", listar_usuarios, ADMIN),
            ("Buscar usuario por id", buscar_usuario_por_id, ADMIN),
        ]),
        "6": ("Indicadores (UF, UTM, dólar)", [
            ("Consultar valor actualizado", consultar_valor_actualizado, TODOS),
            ("Ver historial guardado", ver_historial_guardado, TODOS),
        ]),
    }

def puede_usar(usuario_actual, quien):
    if quien == TODOS:
        return True
    if quien == ADMIN:
        return es_administrador(usuario_actual)
    return not es_administrador(usuario_actual)

def opciones_permitidas(usuario_actual, opciones):
    return [(texto, accion) for texto, accion, quien in opciones if puede_usar(usuario_actual, quien)]

def submenus_visibles(usuario_actual, submenus):
    # Un submenú sin opciones para el rol no se muestra (por ejemplo, Departamentos para un empleado).
    return {numero: (titulo, opciones) for numero, (titulo, opciones) in submenus.items()
            if opciones_permitidas(usuario_actual, opciones)}

def menu(usuario_actual, submenus):
    print(f"\n***** Menú principal ({usuario_actual['nombre_usuario']}, {usuario_actual['rol']}) *****")
    for numero, (titulo, _) in submenus.items():
        print(f"{numero}. {titulo}")
    print("7. Mi perfil")
    print("8. Cerrar sesión")
    print("9. Salir")

def ejecutar_submenu(usuario_actual, titulo, opciones):
    permitidas = opciones_permitidas(usuario_actual, opciones)
    volver = str(len(permitidas) + 1)

    while True:
        print(f"\n--- {titulo} ---")
        for numero, (texto, _) in enumerate(permitidas, start=1):
            print(f"{numero}. {texto}")
        print(f"{volver}. Volver")
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == volver:
            return
        if opcion.isdigit() and 1 <= int(opcion) <= len(permitidas):
            _, accion = permitidas[int(opcion) - 1]
            try:
                accion(usuario_actual)
            except (ErrorBaseDatos, PermissionError) as error:
                print(f"\n{error}")
        else:
            print("\nSeleccione una opción válida")

def menu_principal(usuario_actual):
    if usuario_actual is None:
        print("\nDebe iniciar sesión.")
        return "cerrar_sesion"

    submenus = submenus_visibles(usuario_actual, crear_submenus())

    while True:
        menu(usuario_actual, submenus)
        seleccion = input("\n¿Qué quieres hacer?: ").strip()

        if seleccion == "7":
            mostrar_perfil(usuario_actual)
        elif seleccion == "8":
            return "cerrar_sesion"
        elif seleccion == "9":
            return "salir"
        elif seleccion in submenus:
            titulo, opciones = submenus[seleccion]
            ejecutar_submenu(usuario_actual, titulo, opciones)
        else:
            print("\nSeleccione una opción válida")
