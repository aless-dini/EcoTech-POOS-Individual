import re
from datetime import datetime
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from persistencia.usuario_dao import UsuarioDAO
from dominio.empleado import Empleado

def a_entero_positivo(valor):
    try:
        numero = int(valor)
    except ValueError:
        return None
    if numero >= 1:
        return numero
    return None

def pedir_texto(mensaje, maximo = 100):
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("Este campo no puede quedar vacío")
            continue
        elif len(texto) > maximo:
            print("Este campo no puede tener más de {maximo} carácteres")
            continue
        elif not all(c.isalpha() or c == " " for c in texto):
            print("Este campo solo acepta letras y espacios")
            continue
        return texto


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

def pedir_direccion(mensaje, maximo=100):
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("Este campo no puede quedar vacío")
            continue
        elif len(texto) > maximo:
            print("Este campo no puede tener más de {maximo} carácteres")
            continue
        return texto

def pedir_telefono(mensaje):
    while True:
        telefono = input(mensaje).strip()
        if telefono.isdecimal() and 8 <= len(telefono) <= 12:
            return int(telefono)
        print("El teléfono debe tener solo números (entre 8 y 12 dígitos), intente de nuevo.")

def pedir_correo(mensaje, id_actual=None):
    while True:
        correo = input(mensaje).strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            print("El correo no es válido (ejemplo: nombre@dominio.cl), intente de nuevo.")
            continue
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None and existente.id != id_actual:
            print(f"El correo ya está registrado para {existente.nombre} (ID {existente.id}), ingrese otro.")
            continue
        return correo

def pedir_fecha(mensaje):
    while True:
        fecha = input(mensaje).strip()
        try:
            datetime.strptime(fecha, "%d-%m-%Y")
            return fecha
        except ValueError:
            print("La fecha debe tener el formato DD-MM-AAAA (ejemplo: 15-03-2024), intente de nuevo.")

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
    nombre = pedir_texto("\nNombre: ")
    direccion = pedir_direccion("Dirección (calle y número): ")
    telefono = pedir_telefono("Teléfono: ")
    correo = pedir_correo("Correo: ", id_actual)
    salario = pedir_entero("Salario: ")
    inicioContrato = pedir_fecha("Inicio contrato (DD-MM-AAAA): ")
    id_departamento = pedir_departamento("Id del departamento (Enter para dejarlo sin departamento): ")
    return nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento

def gestionar_empleados():
    print("\n1. Registrar empleado")
    print("2. Actualizar empleado")
    print("3. Eliminar empleado")
    print("4. Listar empleados")
    print("5. Listar empleados por departamento")
    print("6. Buscar empleado por id")
    print("7. Buscar empleado por nombre")
    print("8. Volver")

def registrar_empleado():
    nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento = ingresar_datos()

    empleado = Empleado(nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento)
    if EmpleadoDAO.insertar(empleado) is not None:
        print(empleado.mostrar_datos())
        print("\nEmpleado registrado correctamente.")
    else:
        print("\nNo fue posible registrar el empleado.")

def actualizar_empleado():
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

def eliminar_empleado():
    idEmpleado = pedir_entero("Ingrese el id del empleado que desea eliminar: ")
    empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
    if empleado is None:
        print("\nNo existe un empleado con ese id")
        return

    if RegistroTiempoDAO.listar_por_empleado(empleado.id):
        print("\nNo se puede eliminar un empleado que tiene horas registradas")
        return

    for proyecto in ProyectoDAO.listar_por_empleado(empleado.id):
        ProyectoDAO.quitar_empleado(proyecto.id, empleado.id)
        print(f"Quitado del proyecto '{proyecto.nombre}'")

    quitar_gerencias(empleado.id)

    for usuario in UsuarioDAO.listar_todos():
        if usuario.id_empleado == empleado.id:
            usuario.id_empleado = None
            UsuarioDAO.actualizar(usuario)
            print(f"El usuario '{usuario.nombre}' quedó sin empleado asociado")

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

def listar_empleados():
    mostrar_lista(EmpleadoDAO.listar_todos())

def listar_empleados_por_departamento():
    idDepartamento = pedir_entero("Ingrese el id del departamento: ")
    mostrar_lista(EmpleadoDAO.listar_por_departamento(idDepartamento))

def buscar_empleado_por_id():
    idEmpleado = pedir_entero("Ingrese el id del empleado que desea buscar: ")

    empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
    if empleado is not None:
        print("\n" + empleado.agregar_descripcion())
    else:
        print("\nNo se encontró un empleado con ese id")

def buscar_empleado_por_nombre():
    nombre = pedir_texto("Ingrese el nombre del empleado que desea buscar: ")
    mostrar_lista(EmpleadoDAO.buscar_por_nombre(nombre))
