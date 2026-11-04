from entradas import pedir_dato
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from persistencia.usuario_dao import UsuarioDAO
from dominio.empleado import Empleado
from servicios import gestion_empleados
from servicios.mi_cuenta import mi_ficha, actualizar_mis_datos
from servicios.permisos import exigir_admin

def a_entero_positivo(valor):
    try:
        numero = int(valor)
    except ValueError:
        return None
    if numero >= 1:
        return numero
    return None

def pedir_entero(mensaje, minimo=1):
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
        except ValueError:
            print("Debe ingresar un número entero, intente de nuevo.")
            continue
        if numero < minimo:
            print(f"El número debe ser mayor o igual a {minimo}, intente de nuevo.")
            continue
        return numero

def pedir_correo(mensaje, id_actual=None):
    while True:
        correo = pedir_dato(mensaje, Empleado.validar_correo)
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None and existente.id != id_actual:
            print(f"El correo ya está registrado para {existente.nombre} (ID {existente.id}), ingrese otro.")
            continue
        return correo

def pedir_departamento(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor == "":
            return None
        id_departamento = a_entero_positivo(valor)
        if id_departamento is None:
            print("El id del departamento debe ser un número entero positivo, intente de nuevo.")
            continue
        if DepartamentoDAO.buscar_por_id(id_departamento) is None:
            print("No existe un departamento con ese id, intente de nuevo.")
            continue
        return id_departamento

def quitar_gerencias(id_empleado, excepto=None):
    for departamento in DepartamentoDAO.listar_todos():
        if departamento.id_gerente == id_empleado and departamento.id != excepto:
            departamento.id_gerente = None
            DepartamentoDAO.actualizar(departamento)
            print(f"El departamento '{departamento.nombre}' quedó sin gerente")

def ingresar_datos(id_actual=None):
    nombre = pedir_dato("\nNombre: ", Empleado.validar_nombre)
    direccion = pedir_dato("Dirección (calle y número): ", Empleado.validar_direccion)
    telefono = pedir_dato("Teléfono: ", Empleado.validar_telefono)
    correo = pedir_correo("Correo: ", id_actual)
    salario = pedir_dato("Salario: ", Empleado.validar_salario)
    inicioContrato = pedir_dato("Inicio contrato (DD-MM-AAAA): ", Empleado.validar_inicio_contrato)
    id_departamento = pedir_departamento("Id del departamento (Enter para dejarlo sin departamento): ")
    return nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento

def registrar_empleado(usuario_actual):
    exigir_admin(usuario_actual)
    nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento = ingresar_datos()

    empleado = Empleado(nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento)
    if EmpleadoDAO.insertar(empleado) is not None:
        print(empleado.mostrar_datos())
        print("\nEmpleado registrado correctamente.")
    else:
        print("\nNo fue posible registrar el empleado.")

def actualizar_empleado(usuario_actual):
    exigir_admin(usuario_actual)
    idEmpleado = pedir_entero("Ingrese el id del empleado que desea actualizar: ")
    actual = EmpleadoDAO.buscar_por_id(idEmpleado)
    if actual is None:
        print("\nNo existe un empleado con ese id")
        return

    print("\nDatos actuales:")
    print(actual.agregar_descripcion())
    nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento = ingresar_datos(idEmpleado)

    empleado = Empleado(nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento, idEmpleado)

    if EmpleadoDAO.actualizar(empleado):
        quitar_gerencias(empleado.id, excepto=id_departamento)
        print(empleado.mostrar_datos())
        print("\nEmpleado actualizado correctamente")
    else:
        print("\nNo fue posible actualizar al empleado")

def eliminar_empleado(usuario_actual):
    exigir_admin(usuario_actual)
    idEmpleado = pedir_entero("Ingrese el id del empleado que desea eliminar: ")
    empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
    if empleado is None:
        print("\nNo existe un empleado con ese id")
        return
    if empleado.id == usuario_actual["empleado_id"]:
        print("\nNo puede eliminar el empleado de la cuenta con la que inició sesión")
        return

    if RegistroTiempoDAO.listar_por_empleado(empleado.id):
        print("\nNo se puede eliminar un empleado que tiene horas registradas")
        return

    for proyecto in ProyectoDAO.listar_por_empleado(empleado.id):
        ProyectoDAO.quitar_empleado(proyecto.id, empleado.id)
        print(f"Quitado del proyecto '{proyecto.nombre}'")

    quitar_gerencias(empleado.id)

    usuario = UsuarioDAO.buscar_por_empleado(empleado.id)
    if usuario is not None and UsuarioDAO.eliminar(usuario.id):
        print(f"Se eliminó la cuenta '{usuario.nombre_usuario}' del empleado")

    if EmpleadoDAO.eliminar(idEmpleado):
        print("\nEmpleado eliminado correctamente")
    else:
        print("\nNo fue posible eliminar al empleado")

def mostrar_lista(empleados):
    if not empleados:
        print("\nNo se encontraron empleados.")
        return
    for empleado in empleados:
        print(empleado.mostrar_datos())

def listar_empleados(usuario_actual):
    mostrar_lista(gestion_empleados.listar_todos(usuario_actual))

def listar_empleados_por_departamento(usuario_actual):
    exigir_admin(usuario_actual)
    idDepartamento = pedir_entero("Ingrese el id del departamento: ")
    mostrar_lista(gestion_empleados.listar_por_departamento(usuario_actual, idDepartamento))

def buscar_empleado_por_id(usuario_actual):
    exigir_admin(usuario_actual)
    idEmpleado = pedir_entero("Ingrese el id del empleado que desea buscar: ")

    empleado = gestion_empleados.buscar_por_id(usuario_actual, idEmpleado)
    if empleado is None:
        print("\nNo se encontró un empleado con ese id")
    else:
        print("\n" + empleado.agregar_descripcion())

def buscar_empleado_por_nombre(usuario_actual):
    exigir_admin(usuario_actual)
    nombre = pedir_dato("Ingrese el nombre del empleado que desea buscar: ", Empleado.validar_nombre)
    mostrar_lista(gestion_empleados.buscar_por_nombre(usuario_actual, nombre))

def mostrar_mi_ficha(usuario_actual):
    try:
        empleado = mi_ficha(usuario_actual)
    except (PermissionError, ValueError) as error:
        print(f"\n{error}")
        return
    print(empleado.mostrar_datos())

def editar_mis_datos(usuario_actual):
    nombre = pedir_dato("\nNuevo nombre: ", Empleado.validar_nombre)
    correo = pedir_correo("Nuevo correo: ", usuario_actual["empleado_id"])
    try:
        actualizado = actualizar_mis_datos(usuario_actual, nombre, correo)
    except (PermissionError, ValueError) as error:
        print(f"\n{error}")
        return
    if actualizado:
        print("\nSus datos se actualizaron correctamente")
    else:
        print("\nNo fue posible actualizar sus datos")
