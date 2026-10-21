from menus.menuEmpleado import (
    gestionar_empleados, registrar_empleado, actualizar_empleado, eliminar_empleado,
    listar_empleados, listar_empleados_por_departamento,
    buscar_empleado_por_id, buscar_empleado_por_nombre,
)
from menus.menuDepartamento import (
    gestionar_departamentos, crear_departamento, eliminar_departamento,
    agregar_empleado_departamento, quitar_empleado_departamento,
    listar_empleados_departamento, ver_cantidad_empleados, editar_departamento,
)
from menus.menuProyecto import (
    gestionar_proyectos, crear_proyecto, editar_proyecto, eliminar_proyecto,
    listar_proyectos, buscar_proyecto_por_id, asignar_empleado_proyecto,
    quitar_empleado_proyecto, listar_empleados_proyecto,
)
from menus.menuRegistroTiempo import (
    gestionar_registros, registrar_horas, editar_registro, eliminar_registro,
    listar_registros, listar_registros_empleado, listar_registros_proyecto,
    exportar_informe_empleado,
)
from menus.menuUsuario import (
    gestionar_usuarios, registrar_usuario, iniciar_sesion, cambiar_contraseña,
    editar_usuario, eliminar_usuario, listar_usuarios,
)

SUBMENUS = {
    "1": (gestionar_empleados, {
        "1": registrar_empleado,
        "2": actualizar_empleado,
        "3": eliminar_empleado,
        "4": listar_empleados,
        "5": listar_empleados_por_departamento,
        "6": buscar_empleado_por_id,
        "7": buscar_empleado_por_nombre,
    }),
    "2": (gestionar_departamentos, {
        "1": crear_departamento,
        "2": eliminar_departamento,
        "3": agregar_empleado_departamento,
        "4": quitar_empleado_departamento,
        "5": listar_empleados_departamento,
        "6": ver_cantidad_empleados,
        "7": editar_departamento,
    }),
    "3": (gestionar_proyectos, {
        "1": crear_proyecto,
        "2": editar_proyecto,
        "3": eliminar_proyecto,
        "4": listar_proyectos,
        "5": buscar_proyecto_por_id,
        "6": asignar_empleado_proyecto,
        "7": quitar_empleado_proyecto,
        "8": listar_empleados_proyecto,
    }),
    "4": (gestionar_registros, {
        "1": registrar_horas,
        "2": editar_registro,
        "3": eliminar_registro,
        "4": listar_registros,
        "5": listar_registros_empleado,
        "6": listar_registros_proyecto,
        "7": exportar_informe_empleado,
    }),
    "5": (gestionar_usuarios, {
        "1": registrar_usuario,
        "2": iniciar_sesion,
        "3": cambiar_contraseña,
        "4": editar_usuario,
        "5": eliminar_usuario,
        "6": listar_usuarios,
    }),
}

def menu():
    print("\n***** Menú principal *****")
    print("1. Gestionar empleados")
    print("2. Gestionar departamentos")
    print("3. Gestionar proyectos")
    print("4. Gestionar registros de tiempo")
    print("5. Gestionar usuarios")
    print("6. Salir")

def ejecutar_submenu(mostrar_opciones, acciones):
    volver = str(len(acciones) + 1)

    while True:
        mostrar_opciones()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == volver:
            return
        if opcion in acciones:
            acciones[opcion]()
        else:
            print("\nSeleccione una opción válida")

def menu_principal():
    print("\n*****Bienvenido al programa de Ecotech*****")

    while True:
        menu()
        seleccion = input("\n¿Qué quieres hacer?: ").strip()

        if seleccion == "6":
            print("Hasta luego!")
            break
        if seleccion in SUBMENUS:
            mostrar_opciones, acciones = SUBMENUS[seleccion]
            ejecutar_submenu(mostrar_opciones, acciones)
        else:
            print("\nSeleccione una opción válida")
