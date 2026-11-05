import os
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from dominio.usuario import Usuario
from persistencia.crear_bd import crear_tablas
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.errores import ErrorBaseDatos
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import crear_cuenta
from servicios.registros import esta_asignado

DEPARTAMENTOS = [
    "Recursos Humanos",
    "Finanzas",
    "Desarrollo",
    "Soporte",
    "Marketing",
]

EMPLEADOS = [
    ("Ana Torres", "Av Providencia 1234", 912345601, "ana.torres@ecotech.example", 1450000, "10-01-2022", "Recursos Humanos"),
    ("Bruno Díaz", "Los Olmos 456", 912345602, "bruno.diaz@ecotech.example", 950000, "03-05-2023", "Recursos Humanos"),
    ("Carla Muñoz", "Pasaje Las Rosas 78", 912345603, "carla.munoz@ecotech.example", 880000, "15-08-2023", "Recursos Humanos"),
    ("Diego Rojas", "Av Matta 2010", 912345604, "diego.rojas@ecotech.example", 820000, "01-02-2024", "Recursos Humanos"),
    ("Elena Soto", "Calle Huérfanos 1500", 912345605, "elena.soto@ecotech.example", 1600000, "20-03-2021", "Finanzas"),
    ("Felipe Vargas", "Av Grecia 3300", 912345606, "felipe.vargas@ecotech.example", 1100000, "11-11-2022", "Finanzas"),
    ("Gabriela Pérez", "Los Aromos 89", 912345607, "gabriela.perez@ecotech.example", 1050000, "07-06-2023", "Finanzas"),
    ("Hugo Castro", "Av Irarrázaval 4500", 912345608, "hugo.castro@ecotech.example", 900000, "18-09-2024", "Finanzas"),
    ("Isabel Fuentes", "Av Apoquindo 5600", 912345609, "isabel.fuentes@ecotech.example", 2100000, "05-04-2020", "Desarrollo"),
    ("Javier Morales", "Calle Moneda 920", 912345610, "javier.morales@ecotech.example", 1700000, "22-07-2021", "Desarrollo"),
    ("Karen Silva", "Los Pinos 345", 912345611, "karen.silva@ecotech.example", 1550000, "14-01-2022", "Desarrollo"),
    ("Luis Herrera", "Av Vicuña Mackenna 7800", 912345612, "luis.herrera@ecotech.example", 1300000, "30-10-2023", "Desarrollo"),
    ("María González", "Av Los Leones 1100", 912345613, "maria.gonzalez@ecotech.example", 1250000, "09-09-2021", "Soporte"),
    ("Nicolás Reyes", "Calle San Diego 650", 912345614, "nicolas.reyes@ecotech.example", 780000, "17-02-2023", "Soporte"),
    ("Olivia Contreras", "Pasaje El Roble 12", 912345615, "olivia.contreras@ecotech.example", 760000, "25-05-2024", "Soporte"),
    ("Pablo Navarro", "Av Departamental 2300", 912345616, "pablo.navarro@ecotech.example", 740000, "02-12-2024", "Soporte"),
    ("Rocío Espinoza", "Av Italia 1450", 912345617, "rocio.espinoza@ecotech.example", 1400000, "12-03-2022", "Marketing"),
    ("Sebastián Tapia", "Calle Lira 380", 912345618, "sebastian.tapia@ecotech.example", 980000, "19-06-2023", "Marketing"),
    ("Tamara Vega", "Los Castaños 77", 912345619, "tamara.vega@ecotech.example", 920000, "28-08-2023", "Marketing"),
    ("Ulises Cárdenas", "Av Pajaritos 3900", 912345620, "ulises.cardenas@ecotech.example", 860000, "04-03-2025", "Marketing"),
]

ADMIN_EMPLEADO = ("Administrador EcoTech", "Av Providencia 1000", 912345600, "admin@ecotech.example", 1500000, "01-01-2020")
ADMIN_USUARIO = "admin"

PROYECTOS = [
    ("Portal web EcoTech", "Sitio público con los servicios de la empresa", "01-03-2025"),
    ("Huella de carbono", "Cálculo de emisiones para clientes", "15-06-2025"),
    ("Migración a la nube", "Traslado de los sistemas internos", "01-09-2025"),
]

# (correo del empleado, nombre del proyecto)
ASIGNACIONES = [
    ("ana.torres@ecotech.example", "Portal web EcoTech"),
    ("ana.torres@ecotech.example", "Huella de carbono"),
    ("bruno.diaz@ecotech.example", "Migración a la nube"),
    ("isabel.fuentes@ecotech.example", "Portal web EcoTech"),
    ("javier.morales@ecotech.example", "Migración a la nube"),
]

# Cuentas habituales (rol empleado / funcionario) vinculadas a empleados de la semilla.
CUENTAS_EMPLEADO = [
    ("ana_torres", "ana.torres@ecotech.example"),
    ("bruno_diaz", "bruno.diaz@ecotech.example"),
]


def cargar_departamentos():
    ids = {}
    for nombre in DEPARTAMENTOS:
        existente = DepartamentoDAO.buscar_por_nombre(nombre)
        if existente is not None:
            print(f"Ya existe el departamento: {nombre}")
            ids[nombre] = existente.id
            continue
        departamento = DepartamentoDAO.insertar(Departamento(nombre, None))
        if departamento is None:
            print(f"No fue posible crear el departamento: {nombre}")
            continue
        print(f"Departamento creado: {nombre}")
        ids[nombre] = departamento.id
    return ids


def cargar_empleados(ids_departamentos):
    creados = 0
    for nombre, direccion, telefono, correo, salario, inicioContrato, nombre_depto in EMPLEADOS:
        if EmpleadoDAO.buscar_por_correo(correo) is not None:
            print(f"Ya existe el empleado: {correo}")
            continue
        id_departamento = ids_departamentos.get(nombre_depto)
        if id_departamento is None:
            print(f"Se omite {correo}: no existe el departamento '{nombre_depto}'")
            continue
        empleado = Empleado(nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento)
        if EmpleadoDAO.insertar(empleado) is None:
            print(f"No fue posible crear el empleado: {correo}")
            continue
        print(f"Empleado creado: {correo}")
        creados += 1
    return creados


def asignar_gerentes(ids_departamentos):
    for nombre_depto, id_departamento in ids_departamentos.items():
        departamento = DepartamentoDAO.buscar_por_id(id_departamento)
        if departamento is None or departamento.id_gerente is not None:
            continue
        correo_gerente = next(e[3] for e in EMPLEADOS if e[6] == nombre_depto)
        gerente = EmpleadoDAO.buscar_por_correo(correo_gerente)
        if gerente is None:
            continue
        departamento.id_gerente = gerente.id
        if DepartamentoDAO.actualizar(departamento):
            print(f"Gerente de {nombre_depto}: {gerente.nombre}")


def cargar_proyectos():
    existentes = {proyecto.nombre: proyecto.id for proyecto in ProyectoDAO.listar_todos()}
    for nombre, descripcion, fecha_inicio in PROYECTOS:
        if nombre in existentes:
            print(f"Ya existe el proyecto: {nombre}")
            continue
        proyecto = ProyectoDAO.insertar(Proyecto(nombre, descripcion, fecha_inicio))
        if proyecto is None:
            print(f"No fue posible crear el proyecto: {nombre}")
            continue
        print(f"Proyecto creado: {nombre}")
        existentes[nombre] = proyecto.id
    return existentes


def asignar_proyectos(ids_proyectos):
    for correo, nombre_proyecto in ASIGNACIONES:
        empleado = EmpleadoDAO.buscar_por_correo(correo)
        id_proyecto = ids_proyectos.get(nombre_proyecto)
        if empleado is None or id_proyecto is None or esta_asignado(empleado.id, id_proyecto):
            continue
        if ProyectoDAO.asignar_empleado(id_proyecto, empleado.id):
            print(f"{empleado.nombre} asignado a '{nombre_proyecto}'")


def leer_clave(variable):
    # Devuelve (clave, sin_clave) o None si la clave del .env no cumple las reglas.
    clave = os.getenv(variable)
    if not clave:
        return None, True
    try:
        Usuario.validar_clave(clave)
    except (TypeError, ValueError) as error:
        print(f"{variable} del archivo .env no es válida: {error}")
        return None
    return clave, False


def cargar_cuentas_empleado():
    # Si la cuenta ya existe no se toca: repetir la semilla no reinicia contraseñas ni roles.
    leida = leer_clave("EMPLEADO_PASSWORD")
    if leida is None:
        return
    clave, sin_clave = leida
    for nombre_usuario, correo in CUENTAS_EMPLEADO:
        if UsuarioDAO.buscar_por_nombre(nombre_usuario) is not None:
            print(f"Ya existe la cuenta: {nombre_usuario}")
            continue
        empleado = EmpleadoDAO.buscar_por_correo(correo)
        if empleado is None:
            print(f"Se omite la cuenta {nombre_usuario}: no existe el empleado {correo}")
            continue
        try:
            crear_cuenta(empleado.id, nombre_usuario, clave, "empleado", sin_clave)
        except (TypeError, ValueError) as error:
            print(f"No fue posible crear la cuenta {nombre_usuario}: {error}")
            continue
        print(f"Cuenta de empleado creada: {nombre_usuario} ({empleado.nombre})")
    if sin_clave:
        print("Las cuentas de empleado nuevas no tienen contraseña (falta EMPLEADO_PASSWORD en el .env).")


def cargar_cuenta_admin():
    if UsuarioDAO.buscar_por_nombre(ADMIN_USUARIO) is not None:
        return True

    leida = leer_clave("ADMIN_PASSWORD")
    if leida is None:
        return False
    clave, sin_clave = leida

    correo = ADMIN_EMPLEADO[3]
    empleado = EmpleadoDAO.buscar_por_correo(correo)
    if empleado is None:
        empleado = EmpleadoDAO.insertar(Empleado(*ADMIN_EMPLEADO))
        if empleado is None:
            print("No fue posible crear el empleado admin")
            return False
        print(f"Empleado creado: {correo}")

    try:
        usuario_id = crear_cuenta(empleado.id, ADMIN_USUARIO, clave, "admin", sin_clave)
    except (TypeError, ValueError) as error:
        print(f"No fue posible crear la cuenta admin: {error}")
        return False
    print(f"Cuenta '{ADMIN_USUARIO}' creada con id {usuario_id}")
    if sin_clave:
        print("La cuenta no tiene contraseña: presione Enter al pedirla y cámbiela después.")
    return True


def cargar_semilla():
    crear_tablas()
    ids_departamentos = cargar_departamentos()
    creados = cargar_empleados(ids_departamentos)
    asignar_gerentes(ids_departamentos)
    asignar_proyectos(cargar_proyectos())
    if cargar_cuenta_admin():
        print(f"Cuenta '{ADMIN_USUARIO}' lista para iniciar sesión")
    cargar_cuentas_empleado()
    print(f"\nEmpleados nuevos en esta ejecución: {creados}")
    print(f"Total departamentos: {len(DepartamentoDAO.listar_todos())}")
    print(f"Total empleados: {len(EmpleadoDAO.listar_todos())}")
    print(f"Total proyectos: {len(ProyectoDAO.listar_todos())}")
    print(f"Total usuarios: {len(UsuarioDAO.listar_todos())}")


if __name__ == "__main__":
    try:
        cargar_semilla()
    except ErrorBaseDatos as error:
        print(error)
