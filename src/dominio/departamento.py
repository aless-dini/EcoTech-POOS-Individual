from dominio.empleado import Empleado

class Departamento:
    def __init__(self, nombre: str, id_gerente: int, id = None):
        self.id = id
        self.nombre = nombre
        self.id_gerente = id_gerente
        self._empleados:list[Empleado] = []

    def agregar_empleado(self, empleado:Empleado) -> bool:
        if empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True
    
    def eliminar_empleado(self, empleado: Empleado) -> bool:
        if empleado not in self._empleados:
            return False
        self._empleados.remove(empleado)
        return True

    def empleados(self) -> tuple:
        return tuple(self._empleados)
 
    def cantidad_empleados(self) -> int:
        return len(self._empleados)


