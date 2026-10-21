class Proyecto :
    def __init__(self, nombre: str, descripcion: str, fechaInicio: str, id = None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        self._empleados: list = []

    def asignar_empleado(self, empleado) -> bool:
        if empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True
 
    def eliminar_empleado(self, empleado) -> bool:
        if empleado not in self._empleados:
            return False
        self._empleados.remove(empleado)
        return True

