from dominio.departamento import Departamento
from dominio.empleado import Empleado
from persistencia.crear_bd import crear_tablas
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO

# Datos ficticios. El nombre identifica al departamento y el correo al empleado,
# así la semilla puede ejecutarse varias veces sin duplicar registros.
DEPARTAMENTOS = [
    "Recursos Humanos",
    "Finanzas",
    "Desarrollo",
    "Soporte",
    "Marketing",
]

# (nombre, direccion, telefono, correo, salario, inicioContrato, departamento)
# El primer empleado de cada departamento queda como gerente.
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


def cargar_semilla():
    crear_tablas()
    ids_departamentos = cargar_departamentos()
    creados = cargar_empleados(ids_departamentos)
    asignar_gerentes(ids_departamentos)
    print(f"\nEmpleados nuevos en esta ejecución: {creados}")
    print(f"Total departamentos: {len(DepartamentoDAO.listar_todos())}")
    print(f"Total empleados: {len(EmpleadoDAO.listar_todos())}")


if __name__ == "__main__":
    cargar_semilla()
