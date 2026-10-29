from dominio.validaciones import LETRAS_Y_NUMEROS, validar_texto, validar_fecha

class Proyecto :
    MAX_NOMBRE = 100
    MAX_DESCRIPCION = 100

    def __init__(self, nombre: str, descripcion: str, fechaInicio: str, id = None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        self._empleados: list = []

    @classmethod
    def validar_nombre(cls, nombre):
        return validar_texto(nombre, "El nombre del proyecto", cls.MAX_NOMBRE, minimo=2, caracteres=LETRAS_Y_NUMEROS)

    @classmethod
    def validar_descripcion(cls, descripcion):
        return validar_texto(descripcion, "La descripción", cls.MAX_DESCRIPCION, minimo=3)

    @staticmethod
    def validar_fecha_inicio(fecha):
        return validar_fecha(fecha, "La fecha de inicio")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_nombre(valor)

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = self.validar_descripcion(valor)

    @property
    def fechaInicio(self):
        return self._fechaInicio

    @fechaInicio.setter
    def fechaInicio(self, valor):
        self._fechaInicio = self.validar_fecha_inicio(valor)

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

    def empleados(self) -> tuple:
        return tuple(self._empleados)
