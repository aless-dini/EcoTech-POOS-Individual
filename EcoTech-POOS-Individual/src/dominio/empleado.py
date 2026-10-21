class Empleado:
    def __init__(self, nombre: str, direccion: str, telefono: int, correo: str, salario: int, inicioContrato: str, id_departamento: int = None, id = None):
        self.id = id
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.salario = salario
        self.inicioContrato = inicioContrato

    def mostrar_datos(self) -> str:
        return f"\nId {self.id}, Nombre {self.nombre}, Correo {self.correo}"

    def actualizar_nombre(self, nombre):
        self.nombre = nombre

    def agregar_descripcion(self) -> str:
        return (f"Empleado {self.nombre} (ID {self.id}) - {self.correo}\n"
                f"Dirección: {self.direccion} | Teléfono: {self.telefono}\n"
                f"Salario: {self.salario} | Inicio contrato: {self.inicioContrato} | "
                f"Departamento: {self.id_departamento if self.id_departamento is not None else 'Sin departamento'}")
