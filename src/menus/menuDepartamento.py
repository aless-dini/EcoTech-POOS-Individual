from dominio.departamento import Departamento
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from menus.menuEmpleado import (
    pedir_texto, pedir_entero, mostrar_lista, a_entero_positivo, quitar_gerencias,
)

def pedir_departamento_existente(mensaje):
    idDepartamento = pedir_entero(mensaje)
    departamento = DepartamentoDAO.buscar_por_id(idDepartamento)
    if departamento is None:
        print("\nNo existe un departamento con ese id")
    return departamento

def pedir_gerente(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor == "":
            return None
        id_gerente = a_entero_positivo(valor)
        if id_gerente is None:
            print("El id del gerente debe ser un número entero positivo, intente de nuevo.")
            continue
        if EmpleadoDAO.buscar_por_id(id_gerente) is None:
            print("No existe un empleado con ese id, intente de nuevo.")
            continue
        return id_gerente

def crear_departamento():
    nombre = pedir_texto("\nNombre del departamento: ")
    id_gerente = pedir_gerente("Id del empleado gerente (Enter para dejarlo sin gerente): ")

    departamento = Departamento(nombre, id_gerente)
    if DepartamentoDAO.insertar(departamento) is not None:
        print(f"\nDepartamento '{departamento.nombre}' creado correctamente con id {departamento.id}")
    else:
        print("\nNo fue posible crear el departamento")

def eliminar_departamento():
    departamento = pedir_departamento_existente("Ingrese el id del departamento que desea eliminar: ")
    if departamento is None:
        return

    if EmpleadoDAO.listar_por_departamento(departamento.id):
        print("\nNo se puede eliminar un departamento que tiene empleados, primero quítelos del departamento")
        return

    if DepartamentoDAO.eliminar(departamento.id):
        print("\nDepartamento eliminado correctamente")
    else:
        print("\nNo fue posible eliminar el departamento")

def agregar_empleado_departamento():
    departamento = pedir_departamento_existente("Ingrese el id del departamento: ")
    if departamento is None:
        return

    idEmpleado = pedir_entero("Ingrese el id del empleado que desea agregar: ")
    empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
    if empleado is None:
        print("\nNo existe un empleado con ese id")
        return
    if empleado.id_departamento == departamento.id:
        print("\nEl empleado ya pertenece a este departamento")
        return

    if EmpleadoDAO.asignar_departamento(empleado.id, departamento.id):
        print(f"\nEmpleado {empleado.nombre} agregado al departamento '{departamento.nombre}'")
        quitar_gerencias(empleado.id, excepto=departamento.id)
    else:
        print("\nNo fue posible agregar el empleado al departamento")

def quitar_empleado_departamento():
    departamento = pedir_departamento_existente("Ingrese el id del departamento: ")
    if departamento is None:
        return

    idEmpleado = pedir_entero("Ingrese el id del empleado que desea quitar: ")
    empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
    if empleado is None:
        print("\nNo existe un empleado con ese id")
        return
    if empleado.id_departamento != departamento.id:
        print("\nEl empleado no pertenece a este departamento")
        return

    if EmpleadoDAO.asignar_departamento(empleado.id, None):
        print(f"\nEmpleado {empleado.nombre} quitado del departamento '{departamento.nombre}'")
        if departamento.id_gerente == empleado.id:
            departamento.id_gerente = None
            DepartamentoDAO.actualizar(departamento)
            print("El departamento quedó sin gerente")
    else:
        print("\nNo fue posible quitar el empleado del departamento")

def listar_empleados_departamento():
    departamento = pedir_departamento_existente("Ingrese el id del departamento: ")
    if departamento is None:
        return

    mostrar_lista(EmpleadoDAO.listar_por_departamento(departamento.id))

def ver_cantidad_empleados():
    departamento = pedir_departamento_existente("Ingrese el id del departamento: ")
    if departamento is None:
        return

    for empleado in EmpleadoDAO.listar_por_departamento(departamento.id):
        departamento.agregar_empleado(empleado)
    print(f"\nEl departamento '{departamento.nombre}' tiene {departamento.cantidad_empleados()} empleado(s)")

def editar_departamento():
    departamento = pedir_departamento_existente("Ingrese el id del departamento que desea editar: ")
    if departamento is None:
        return

    if departamento.id_gerente is None:
        gerente = "Sin gerente"
    else:
        empleado = EmpleadoDAO.buscar_por_id(departamento.id_gerente)
        gerente = f"{empleado.nombre} (id {empleado.id})" if empleado else departamento.id_gerente

    print("\nDatos actuales:")
    print(f"Id: {departamento.id} | Nombre: {departamento.nombre} | Gerente: {gerente}")

    nombre = input(f"\nNuevo nombre (Enter para mantener '{departamento.nombre}'): ").strip()
    if nombre:
        departamento.nombre = nombre

    while True:
        valor = input("Id del nuevo gerente (Enter para mantener el actual, 0 para dejarlo sin gerente): ").strip()
        if valor == "":
            break
        if valor == "0":
            departamento.id_gerente = None
            break
        id_gerente = a_entero_positivo(valor)
        if id_gerente is None:
            print("El id del gerente debe ser un número entero positivo, intente de nuevo.")
            continue
        empleado = EmpleadoDAO.buscar_por_id(id_gerente)
        if empleado is None:
            print("No existe un empleado con ese id, intente de nuevo.")
            continue
        if empleado.id_departamento != departamento.id:
            print("El gerente debe pertenecer a este departamento, intente de nuevo.")
            continue
        departamento.id_gerente = empleado.id
        break

    if DepartamentoDAO.actualizar(departamento):
        print("\nDepartamento actualizado correctamente")
    else:
        print("\nNo fue posible actualizar el departamento")
