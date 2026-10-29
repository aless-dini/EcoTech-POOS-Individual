import math
from dominio.validaciones import validar_fecha, validar_id_opcional

class RegistroTiempo:
    MAX_HORAS = 24

    def __init__(self, fecha: str, horas: float, id_empleado: int = None, id_proyecto: int = None, id = None):
        self.id = id
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto
        self.fecha = fecha
        self.horas = horas

    @staticmethod
    def validar_fecha_registro(fecha):
        return validar_fecha(fecha, "La fecha")

    @classmethod
    def validar_horas(cls, horas):
        try:
            horas = float(str(horas).strip().replace(",", "."))
        except ValueError:
            raise ValueError("Debe ingresar un número (por ejemplo 8 o 7,5).") from None
        if not math.isfinite(horas) or not 0 < horas <= cls.MAX_HORAS:
            raise ValueError(f"Las horas deben ser mayores que 0 y como máximo {cls.MAX_HORAS}.")
        return round(horas, 2)

    @property
    def id_empleado(self):
        return self._id_empleado

    @id_empleado.setter
    def id_empleado(self, valor):
        self._id_empleado = validar_id_opcional(valor, "El id del empleado")

    @property
    def id_proyecto(self):
        return self._id_proyecto

    @id_proyecto.setter
    def id_proyecto(self, valor):
        self._id_proyecto = validar_id_opcional(valor, "El id del proyecto")

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = self.validar_fecha_registro(valor)

    @property
    def horas(self):
        return self._horas

    @horas.setter
    def horas(self, valor):
        self._horas = self.validar_horas(valor)

    def mostrar_registro(self) -> str:
        return f"{self.fecha} - {self.horas:g}"

    def realizar_informe(self) -> str:
        return f"Informe de tiempo: {self.fecha} — {self.horas:g} horas trabajadas"

    def exportar_informe(self, ruta: str = "informe_tiempo.txt") -> None:
        with open(ruta, "a", encoding="utf-8") as archivo:
            archivo.write(self.realizar_informe() + "\n")
