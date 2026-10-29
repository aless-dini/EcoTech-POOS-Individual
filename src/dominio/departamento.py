from dominio.empleado import Empleado
from dominio.validaciones import SOLO_LETRAS, validar_texto, validar_id_opcional

class Departamento:
    MAX_NOMBRE = 100

    def __init__(self, nombre: str, id_gerente: int, id = None):
        self.id = id
        self.nombre = nombre
        self.id_gerente = id_gerente
        self._empleados:list[Empleado] = []

    @classmethod
    def validar_nombre(cls, nombre):
        return validar_texto(nombre, "El nombre del departamento", cls.MAX_NOMBRE, minimo=2, caracteres=SOLO_LETRAS)

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_nombre(valor)

    @property
    def id_gerente(self):
        return self._id_gerente

    @id_gerente.setter
    def id_gerente(self, valor):
        self._id_gerente = validar_id_opcional(valor, "El id del gerente")

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
