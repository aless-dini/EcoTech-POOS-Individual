from menus.menuEmpleado import (
    registrar_empleado, actualizar_empleado, eliminar_empleado,
    listar_empleados, listar_empleados_por_departamento,
    buscar_empleado_por_id, buscar_empleado_por_nombre,
)
from menus.menuDepartamento import (
    crear_departamento, eliminar_departamento,
    agregar_empleado_departamento, quitar_empleado_departamento,
    listar_empleados_departamento, ver_cantidad_empleados, editar_departamento,
)
from menus.menuProyecto import (
    crear_proyecto, editar_proyecto, eliminar_proyecto,
    listar_proyectos, buscar_proyecto_por_id, asignar_empleado_proyecto,
    quitar_empleado_proyecto, listar_empleados_proyecto,
)
from menus.menuRegistroTiempo import (
    registrar_horas, editar_registro, eliminar_registro,
    listar_registros, listar_registros_empleado, listar_registros_proyecto,
    exportar_informe_empleado,
)
from menus.menuUsuario import (
    solicitar_registro, cambiar_contraseña, editar_usuario, eliminar_usuario,
    listar_usuarios, buscar_usuario_por_id, mostrar_perfil,
)
from servicios.autenticacion import es_administrador

# Quién puede ver cada opción del menú.
ADMIN = "administrador"
EMPLEADO = "empleado"
TODOS = "todos"

def crear_submenus(usuario_actual):
    # Cada opción es (texto, función, quién puede usarla). Las funciones que
    # necesitan saber quién inició sesión reciben usuario_actual con lambda.
    return {
        "1": ("Empleados", [
            ("Registrar empleado", registrar_empleado, ADMIN),
            ("Actualizar empleado", actualizar_empleado, ADMIN),
            ("Eliminar empleado", eliminar_empleado, ADMIN),
            ("Listar empleados", listar_empleados, TODOS),
            ("Listar empleados por departamento", listar_empleados_por_departamento, TODOS),
            ("Buscar empleado por id", lambda: buscar_empleado_por_id(usuario_actual), TODOS),
            ("Buscar empleado por nombre", buscar_empleado_por_nombre, TODOS),
        ]),
        "2": ("Departamentos", [
            ("Crear departamento", crear_departamento, ADMIN),
            ("Editar departamento", editar_departamento, ADMIN),
            ("Eliminar departamento", eliminar_departamento, ADMIN),
            ("Agregar empleado al departamento", agregar_empleado_departamento, ADMIN),
            ("Quitar empleado del departamento", quitar_empleado_departamento, ADMIN),
            ("Listar empleados del departamento", listar_empleados_departamento, TODOS),
            ("Ver cantidad de empleados", ver_cantidad_empleados, TODOS),
        ]),
        "3": ("Proyectos", [
            ("Crear proyecto", crear_proyecto, ADMIN),
            ("Editar proyecto", editar_proyecto, ADMIN),
            ("Eliminar proyecto", eliminar_proyecto, ADMIN),
            ("Asignar empleado al proyecto", asignar_empleado_proyecto, ADMIN),
            ("Quitar empleado del proyecto", quitar_empleado_proyecto, ADMIN),
            ("Listar proyectos", listar_proyectos, TODOS),
            ("Buscar proyecto por id", buscar_proyecto_por_id, TODOS),
            ("Listar empleados del proyecto", listar_empleados_proyecto, TODOS),
        ]),
        "4": ("Registros de tiempo", [
            ("Registrar horas", lambda: registrar_horas(usuario_actual), ADMIN),
            ("Registrar mis horas", lambda: registrar_horas(usuario_actual), EMPLEADO),
            ("Editar registro", editar_registro, ADMIN),
            ("Eliminar registro", eliminar_registro, ADMIN),
            ("Listar todos los registros", listar_registros, ADMIN),
            ("Listar registros de un empleado", lambda: listar_registros_empleado(usuario_actual), ADMIN),
            ("Ver mis registros", lambda: listar_registros_empleado(usuario_actual), EMPLEADO),
            ("Listar registros de un proyecto", listar_registros_proyecto, ADMIN),
            ("Exportar informe de un empleado", lambda: exportar_informe_empleado(usuario_actual), ADMIN),
            ("Exportar mi informe", lambda: exportar_informe_empleado(usuario_actual), EMPLEADO),
        ]),
        "5": ("Usuarios", [
            ("Registrar usuario", solicitar_registro, ADMIN),
            ("Cambiar mi contraseña", lambda: cambiar_contraseña(usuario_actual), TODOS),
            ("Editar rol de un usuario", editar_usuario, ADMIN),
            ("Eliminar usuario", lambda: eliminar_usuario(usuario_actual), ADMIN),
            ("Listar usuarios", listar_usuarios, ADMIN),
            ("Buscar usuario por id", buscar_usuario_por_id, ADMIN),
        ]),
    }

def puede_usar(usuario_actual, quien):
    if quien == TODOS:
        return True
    if quien == ADMIN:
        return es_administrador(usuario_actual)
    return not es_administrador(usuario_actual)

def menu(usuario_actual, submenus):
    print(f"\n***** Menú principal ({usuario_actual['nombre_usuario']}, {usuario_actual['rol']}) *****")
    for numero, (titulo, _) in submenus.items():
        print(f"{numero}. {titulo}")
    print("6. Mi perfil")
    print("7. Cerrar sesión")
    print("8. Salir")

def ejecutar_submenu(usuario_actual, titulo, opciones):
    # Solo se muestran (y solo se pueden elegir) las opciones permitidas para el rol.
    permitidas = [(texto, accion) for texto, accion, quien in opciones if puede_usar(usuario_actual, quien)]
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
            accion()
        else:
            print("\nSeleccione una opción válida")

def menu_principal(usuario_actual):
    # Devuelve "cerrar_sesion" o "salir" para que main.py decida qué hacer.
    if usuario_actual is None:
        print("\nDebe iniciar sesión.")
        return "cerrar_sesion"

    submenus = crear_submenus(usuario_actual)

    while True:
        menu(usuario_actual, submenus)
        seleccion = input("\n¿Qué quieres hacer?: ").strip()

        if seleccion == "6":
            mostrar_perfil(usuario_actual)
        elif seleccion == "7":
            return "cerrar_sesion"
        elif seleccion == "8":
            return "salir"
        elif seleccion in submenus:
            titulo, opciones = submenus[seleccion]
            ejecutar_submenu(usuario_actual, titulo, opciones)
        else:
            print("\nSeleccione una opción válida")
